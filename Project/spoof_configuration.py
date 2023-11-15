class SpoofConfiguration:
    def __init__(self):
        self.configurations = {}

    def add_spoof_config(self, vehicle_id, field_dict):
        self.configurations[vehicle_id] = field_dict

    def get_spoof_config(self, vehicle_id):
        return self.configurations.get(vehicle_id, None)