import pandas as pd
import time
import random
from vehicle import Vehicle
from misbehaving_vehicle import MisbehavingVehicle
import parse
import json
import misbehavior_detector
from memory_profiler import memory_usage



############################################ setup ############################################################


df = pd.read_csv('event_data.csv')

#create list of ids
vehicle_ids = list(set(df['eventHeader_hostVehID'].unique()).union(df['eventHeader_targetVehID'].unique()))

#random decide which vehicles are misbehaving
num_misbehaving = int(len(vehicle_ids) * 0.5)
misbehaving_ids = random.sample(vehicle_ids, num_misbehaving)

#class allocation
vehicles = {}
for id in vehicle_ids:
    if id in misbehaving_ids:
        vehicles[id] = MisbehavingVehicle(id)
    else:
        vehicles[id] = Vehicle(id)





print("Simulating vehicles sending messages...")
for idx, row in df.iterrows():
    host_vehicle = vehicles.get(row['eventHeader_hostVehID'])
    if host_vehicle:
        bsmList = json.loads(row['bsmList']) #convert bsmlist to dics
        bsm_messages = [parse.create_event_msg_from_dict(bsm_dict) for bsm_dict in bsmList] #convert to eventmsg obj
        
        if isinstance(host_vehicle, MisbehavingVehicle):
            field_dict = {
                ("bsmRecord", "bsmMsg", "coreData", "T_s"): 9.90,
                
            }
            bsm_messages = host_vehicle.spoof_fields(bsm_messages, field_dict)
        host_vehicle.send_message(row['eventHeader_targetVehID'], bsm_messages, vehicles)



detection_times = []

for id, vehicle in vehicles.items():
    start_time = time.perf_counter()
    
    is_consistent = vehicle.check_received_messages_for_misbehavior()
    if not is_consistent:
        vehicle.send_misbehavior_report()
    
    end_time = time.perf_counter()

    if not is_consistent and isinstance(vehicle, MisbehavingVehicle):
        detection_time = end_time - start_time
        if detection_time > 0.0:
            detection_times.append(detection_time)
    
for id, vehicle in vehicles.items():
    is_consistent = vehicle.check_received_messages_for_misbehavior()
    if not is_consistent:
        vehicle.send_misbehavior_report()

if detection_times:
    average_detection_time = sum(detection_times) / len(detection_times)
    min_detection_time = min(detection_times)
    max_detection_time = max(detection_times)



# memory_consumptions = []

# batch_size = 50  # Adjust this based on your requirement
# vehicles_list = list(vehicles.values())
# for i in range(0, len(vehicles_list), batch_size):
#     batch_vehicles = vehicles_list[i:i + batch_size]
    
#     mem_before = memory_usage(-1, interval=1, timeout=1)[0]  # Increase interval for less overhead
    
#     inconsistencies = []
#     for vehicle in batch_vehicles:
#         is_consistent = vehicle.check_received_messages_for_misbehavior()
#         if not is_consistent:
#             inconsistencies.append(True)

#     mem_after = memory_usage(-1, interval=1, timeout=1)[0]

#     if inconsistencies:
#         mem_consumed_per_vehicle = (mem_after - mem_before) / len(inconsistencies)
#         memory_consumptions.extend([mem_consumed_per_vehicle] * len(inconsistencies))

# # Ensure the list isn't empty before doing calculations
# if memory_consumptions:
#     average_memory = sum(memory_consumptions) / len(memory_consumptions)
#     min_memory = min(memory_consumptions)
#     max_memory = max(memory_consumptions)



################################################# Statistics #################################################
misbehaving_percentage = (len(misbehaving_ids) / len(vehicle_ids)) * 100
#print(f"Misbehaving vehicles: {misbehaving_ids}")
print(f"{'*' * 25}" + " Statistics " + "*" * 25)
print(f"Total number of vehicles: {len(vehicle_ids)}")
print(f"Percentage of misbehaving vehicles: {misbehaving_percentage}%")
print("Minimum detection time: {:.10f} seconds".format(min_detection_time))
print("Maximum detection time: {:.10f} seconds".format(max_detection_time))
print("Average detection time: {:.10f} seconds".format(average_detection_time))
# print("Minimum memory consumption: {:.10f} MiB".format(min_memory))
# print("Maximum memory consumption: {:.10f} MiB".format(max_memory))
# print("Average memory consumption: {:.10f} MiB".format(average_memory))
# print(detection_times)