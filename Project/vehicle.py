import misbehavior_detector

class Vehicle:
    def __init__(self, id):
        self.id = id
        self.received_messages = []
        self.sent_messages = []
        self.detector = misbehavior_detector.MisbehaviorDetector()

    def send_message(self, target_vehicle_id, bsm, vehicles):
        #check for self msessage
        if self.id == target_vehicle_id:
            print(f"Warning: Vehicle {self.id} is attempting to send a message to itself.")
            return 

        target_vehicle = vehicles.get(target_vehicle_id)
        if target_vehicle:
            self.sent_messages.append(bsm)
            target_vehicle.receive(self.id, bsm)

    def receive(self, sender_vehicle_id, bsm):
        self.received_messages.append((sender_vehicle_id, bsm))

    def check_received_messages_for_misbehavior(self):
        for sender_vehicle_id, bsm_list in self.received_messages:
            for bsm in bsm_list:
                is_consistent, msg = self.detector.detect_misbehavior(self.id, bsm, sender_vehicle_id)
                if not is_consistent:
                    print(msg)

    def send_misbehavior_report(self, bsm, reason, sender_vehicle_id, severity):
        report_data = {
            "vehicle_id": self.id,
            "sender_vehicle_id": sender_vehicle_id,
            "misbehaving_message": bsm,
            "reason": self.check_received_messages_for_misbehavior(),
            "severity": severity
        }
        self.misbehavior_reporter.submit(report_data)

        def get_all_event_msgs(self):
            return [bsm for _, bsm in self.received_messages]  