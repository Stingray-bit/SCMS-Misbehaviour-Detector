from vehicle import Vehicle
import random
import Utility

class MisbehavingVehicle(Vehicle):
    def __init__(self, id):
        super().__init__(id)
        self.captured_messages = [] 
        
    def spoof_fields(self, bsm, field_dict):
        for event_msg in bsm:
            for field_path, new_value in field_dict.items():
                Utility.set_nested_attr(event_msg, list(field_path), new_value) 
        return bsm

    def change_bsm(self, bsm):
        for event_msg in bsm:
            event_msg.eventMsgSeqNum = "fake message"
        return bsm
    
    def spoof_speed_and_acceleration(self, bsm, speed_multiplier=1.5, acceleration_offset=2.0):
        original_speed = bsm[0].BsmRecord.BsmMsg.CoreData.speed_mps
        original_long_accel = bsm[0].BsmRecord.BsmMsg.CoreData.accelSet.long_mpss
        original_lat_accel = bsm[0].BsmRecord.BsmMsg.CoreData.accelSet.lat_mpss
        original_vert_accel = bsm[0].BsmRecord.BsmMsg.CoreData.accelSet.vert_mpss

        field_dict = {
            ("bsmRecord", "BsmMsg", "CoreData", "speed_mps"): original_speed * speed_multiplier,
            ("bsmRecord", "BsmMsg", "CoreData", "accelSet", "long_mpss"): original_long_accel + acceleration_offset,
            ("bsmRecord", "BsmMsg", "CoreData", "accelSet", "lat_mpss"): original_lat_accel + acceleration_offset,
            ("bsmRecord", "BsmMsg", "CoreData", "accelSet", "vert_mpss"): original_vert_accel + acceleration_offset
        }

        return self.spoof_fields(bsm, field_dict)

    
        def capture_message(self, bsm):
            self.captured_messages.append(bsm)

        def replay_message(self):
            if not self.captured_messages:
                print("No captured messages to replay!")
                return None
            return random.choice(self.captured_messages)
        
        