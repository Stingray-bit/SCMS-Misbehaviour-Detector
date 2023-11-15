import unittest
from spoof_configuration import SpoofConfiguration
from misbehaving_vehicle import MisbehavingVehicle
from parse import EventMsg

class TestSpoofing(unittest.TestCase):
    def setUp(self):
        self.vehicle = MisbehavingVehicle("V001")
        self.spoof_config = SpoofConfiguration()
    
    def test_vehicle_specific_spoofing(self):
        bsm = [EventMsg()]

        self.spoof_config.add_spoof_config(vehicle_id="V001", field_dict={("bsmRecord", "msgHeader", "myRFLevel"): 3.25})

        specific_config = self.spoof_config.get_spoof_config(self.vehicle.id)
        if specific_config:
            bsm = self.vehicle.spoof_fields(bsm, specific_config)

        self.assertEqual(bsm[0].BsmRecord.MsgHeader.myRFLevel, 3.25)

if __name__ == "__main__":
    unittest.main()