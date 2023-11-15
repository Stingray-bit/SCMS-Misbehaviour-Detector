import json

class Accuracy:
    def __init__(self, semiMajor, semiMinor, orientation):
        self.semiMajor = semiMajor
        self.semiMinor = semiMinor
        self.orientation = orientation

class AccelSet:
    def __init__(self, long_mpss, lat_mpss, vert_mpss, yaw_dps):
        self.long_mpss = long_mpss
        self.lat_mpss = lat_mpss
        self.vert_mpss = vert_mpss
        self.yaw_dps = yaw_dps

class Brakes:
    def __init__(self, wheelBrakes, traction, abs, scs, brakeBoost, auxBrakes):
        self.wheelBrakes = wheelBrakes
        self.traction = traction
        self.abs = abs
        self.scs = scs
        self.brakeBoost = brakeBoost
        self.auxBrakes = auxBrakes

class Size:
    def __init__(self, width, length):
        self.width = width
        self.length = length

class CrumbData:
    def __init__(self, xOffset_m, yOffset_m, zOffset_m, tOffset_s):
        self.xOffset_m = xOffset_m
        self.yOffset_m = yOffset_m
        self.zOffset_m = zOffset_m
        self.tOffset_s = tOffset_s

class PathHistory:
    def __init__(self, crumbData):
        self.crumbData = [CrumbData(**cd) for cd in crumbData]

class PathPrediction:
    def __init__(self, radiusOfCurve, confidence):
        self.radiusOfCurve = radiusOfCurve
        self.confidence = confidence

class VehicleData:
    def __init__(self, height, mass=None):
        self.height = height
        self.mass = mass


class PartIIValue:
    def __init__(self, classification=None, vehicleData=None, pathHistory=None, pathPrediction=None, lights=None, events = None):
        self.classification = classification
        self.vehicleData = VehicleData(**vehicleData) if vehicleData else None
        self.pathHistory = PathHistory(**pathHistory) if pathHistory else None
        self.pathPrediction = PathPrediction(**pathPrediction) if pathPrediction else None
        self.lights = lights
        self.events = events


class PartII:
    def __init__(self, partII_Id, partII_Value):
        self.partII_Id = partII_Id
        self.partII_Value = PartIIValue(**partII_Value)

class CoreData:
    def __init__(self, msgCnt, id, accuracy, transmission, angle, accelSet, brakes, size, X_m, Y_m, Z_m, T_s, speed_mps, heading_deg):
        self.msgCnt = msgCnt
        self.id = id
        self.accuracy = Accuracy(**accuracy)
        self.transmission = transmission
        self.angle = angle
        self.accelSet = AccelSet(**accelSet)
        self.brakes = Brakes(**brakes)
        self.size = Size(**size)
        self.X_m = X_m
        self.Y_m = Y_m
        self.Z_m = Z_m
        self.T_s = T_s
        self.speed_mps = speed_mps
        self.heading_deg = heading_deg

class MsgHeader:
    def __init__(self, myRFLevel, authenticated):
        self.myRFLevel = myRFLevel
        self.authenticated = authenticated

class BsmMsg:
    def __init__(self, coreData, partII):
        self.coreData = CoreData(**coreData)
        self.partII = [PartII(**p) for p in partII]

class BsmRecord:
    def __init__(self, msgHeader, bsmMsg):
        self.msgHeader = MsgHeader(**msgHeader)
        self.bsmMsg = BsmMsg(**bsmMsg)

class EventMsg:
    def __init__(self, eventMsgSeqNum, bsmRecord):
        self.eventMsgSeqNum = eventMsgSeqNum
        self.bsmRecord = BsmRecord(**bsmRecord)

def create_event_msg_from_dict(input_dict):
    # Manually construct bsmRecord.bsmMsg.partII, converting keys
    for p in input_dict['bsmRecord']['bsmMsg']['partII']:
        p['partII_Id'] = p.pop('partII-Id')
        p['partII_Value'] = p.pop('partII-Value')
    return EventMsg(**input_dict)


# input_dict = json.loads(json_str)
# event_msg = create_event_msg_from_dict(input_dict)
# print(event_msg.eventMsgSeqNum) 
# print(event_msg.bsmRecord.msgHeader.myRFLevel)
# print(event_msg.bsmRecord.bsmMsg.coreData.msgCnt) 
# print(event_msg.bsmRecord.bsmMsg.coreData.accuracy.semiMajor)  
# print(event_msg.bsmRecord.bsmMsg.coreData.accelSet.long_mpss)  
# print(event_msg.bsmRecord.bsmMsg.coreData.brakes.wheelBrakes)  
# print(event_msg.bsmRecord.bsmMsg.coreData.size.width)  
# print(event_msg.bsmRecord.bsmMsg.coreData.accelSet.lat_mpss)  
