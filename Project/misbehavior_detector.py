class MisbehaviorDetector:
    
    MAX_ACCELERATION = 50  

    MAX_MESSAGE_RATE = 50 
    MAX_MESSAGE_DELAY = 0.5  

    RSSI_WINDOW_SIZE = 1000000000  
    RSSI_THRESHOLD = 0.0001  
    
    def __init__(self):
        self.historical_data = {} 
        self.rssi_window = [] 
    
    def rssi_consistency(self, vehicle_id, rssi, msg_source):
        """
        Check for potential Sybil attacks based on RSSI values.

        Args:
        - vehicle_id (str): ID of the vehicle.
        - rssi (float): RSSI value of the current message.
        - msg_source: Source of the message.

        Returns:
        - bool: True if no Sybil attack detected, False otherwise.
        - str: Description of the misbehavior if detected.
        """
        
        #add new rssi
        self.rssi_window.append((vehicle_id, rssi)) 

        #if too big remove
        while len(self.rssi_window) > self.RSSI_WINDOW_SIZE:
            self.rssi_window.pop(0)
        
        #count how many ids have similair rsssi
        similar_rssi_ids = set(vid for vid, r in self.rssi_window if abs(r - rssi) <= self.RSSI_THRESHOLD and vid != vehicle_id)

       
        if len(similar_rssi_ids) > 1:  
            return (False, f"[Misbehavior Detected] Vehicle ID: {vehicle_id}, Message Source: {msg_source}, Issue: Potential Sybil Attack Detected, Details: Multiple vehicles with similar RSSI values.")

        return True, ""
    
    def temporal_consistency(self, vehicle_id, timestamp, msg_source):
        WINDOW_SIZE = 50  

        if vehicle_id == "00000000":
            return True, ""

        try:
            timestamp = float(timestamp)
        except ValueError:
            return (False, f"[Misbehavior Detected] Vehicle ID: {vehicle_id}, Message Source: {msg_source}, Issue: Temporal Data Inconsistency, Details: Non-numeric timestamp")

        if vehicle_id not in self.historical_data:
            self.historical_data[vehicle_id] = {
                'timestamp': timestamp,
                'repeated_count': 0,
                'delay_count': 0,
                'rapid_count': 0,
                'time_diff_window': []
            }
            return True, ""

        last_timestamp = self.historical_data[vehicle_id]['timestamp']

        current_time_diff = abs(timestamp - last_timestamp)

        #update window
        if len(self.historical_data[vehicle_id]['time_diff_window']) >= WINDOW_SIZE:
            self.historical_data[vehicle_id]['time_diff_window'].pop(0)
        self.historical_data[vehicle_id]['time_diff_window'].append(current_time_diff)

        avg_time_diff = sum(self.historical_data[vehicle_id]['time_diff_window']) / len(self.historical_data[vehicle_id]['time_diff_window'])

        #replay attcack
        if current_time_diff == 0:
            self.historical_data[vehicle_id]['repeated_count'] += 1
            if self.historical_data[vehicle_id]['repeated_count'] >= 3:
                return (False, f"[Misbehavior Detected] Vehicle ID: {vehicle_id}, Message Source: {msg_source}, Issue: Replay Attack Detected, Details: Repeated Timestamp: {timestamp}")
        else:
            self.historical_data[vehicle_id]['repeated_count'] = 0

        #deviation from average
        DELAY_MULTIPLIER = 100
        RAPID_MULTIPLIER = 0.0001

        if current_time_diff > avg_time_diff * DELAY_MULTIPLIER:
            self.historical_data[vehicle_id]['delay_count'] += 1
            if self.historical_data[vehicle_id]['delay_count'] >= 3:
                return (False, f"[Misbehavior Detected] Vehicle ID: {vehicle_id}, Message Source: {msg_source}, Issue: Delay Attack Detected, Details: Significant delay in messages received consecutively.")
        else:
            self.historical_data[vehicle_id]['delay_count'] = 0

        if current_time_diff < avg_time_diff * RAPID_MULTIPLIER:
            self.historical_data[vehicle_id]['rapid_count'] += 1
            if self.historical_data[vehicle_id]['rapid_count'] >= 3:
                return (False, f"[Misbehavior Detected] Vehicle ID: {vehicle_id}, Message Source: {msg_source}, Issue: Flooding Attack Detected, Details: Rapid messages received consecutively.")
        else:
            self.historical_data[vehicle_id]['rapid_count'] = 0

        self.historical_data[vehicle_id]['timestamp'] = timestamp

        return True, ""

    def acceleration_consistency(self, vehicle_id, acceleration, msg_source):
        if vehicle_id == "00000000":
            return True, ""
        try:
            acceleration = float(acceleration)
        except ValueError:
            return (False, f"[Misbehavior Detected] Vehicle ID: {vehicle_id}, Message Source: {msg_source}, Issue: Acceleration Data Inconsistency, Details: Non-numeric acceleration")

        if abs(acceleration) > self.MAX_ACCELERATION:
            return (False, f"[Misbehavior Detected] Vehicle ID: {vehicle_id}, Message Source: {msg_source}, Issue: Acceleration Inconsistency, Details: Reported Acceleration: {acceleration}")
        return True, ""


    def detect_misbehavior(self, vehicle_id, event_msg, msg_source):
        core_data = event_msg.bsmRecord.bsmMsg.coreData

        temporal_result, temporal_message = self.temporal_consistency(vehicle_id, core_data.T_s, msg_source)
        acceleration_result, acceleration_message = self.acceleration_consistency(vehicle_id, core_data.accelSet.long_mpss, msg_source)
        # sybil_result, sybil_message = self.rssi_consistency(vehicle_id, event_msg.bsmRecord.msgHeader.myRFLevel, msg_source)
        
        if not temporal_result:
            return False, temporal_message
        if not acceleration_result:
            return False, acceleration_message
        # if not sybil_result:
            # return False, sybil_message
        
        return True, "No Misbehavior Detected"
