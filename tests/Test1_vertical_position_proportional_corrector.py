"""
Test vertical positionning with vertical lidars in real Drone and
proportional corrector
"""

import sys
import time
import argparse
import numpy as np

sys.path.insert(0, '../drone')

from inspection_drone_vertical_mov import InspectionDroneVertical

parser = argparse.ArgumentParser(description='commands')
parser.add_argument('--connect')
args = parser.parse_args()

connection_string = args.connect

# Connection between the Raspberry and the Pixhawk
drone = InspectionDroneVertical('/dev/serial0', baudrate=115200,
                                two_way_switches=[7, 8], three_way_switches=[5, 6, 9, 10, 11, 12],
                                lidar_address=[0x10], lidar_angle=[0], lidar_vertical_address=[0x13, 0x17],
                                lidar_vertical_position=[0, 1], critical_distance_lidar=100)

V_command = 0              #Velocity to command the drone
K = 0.0025                  #Coefficient for the PID
target_distance = 150      #The drone must stop at this distance from the obstacle
measured_distance = -1     #Data from the sensor

drone.launch_mission()

print("sleep 10 sec to start mission")
time.sleep(10)
print("starting mission")
time_0 = time.time()

drone.set_guided_mode()
drone.send_mavlink_stay_stationary()
while drone.mission_running():
    drone.update_time()  # update time since connexion and mission's start
    mission_time = time.time() - time_0
    drone.update_switch_states() # update the RC transmitter switch state

    if drone.vertical_lidars.get_up_lidar().lidar_reading():
        drone.vertical_lidars.read_down_distance()
        measured_distance = drone.vertical_lidars.get_down_distance()
        print("lidar down reading")
        print(measured_distance)
        V_command = K * (measured_distance - target_distance)
        print("Velocity Z command")
        print(V_command)
        V_command = np.min([np.abs(V_command), 0.5]) * np.sign(V_command)

    drone.send_mavlink_go_down(V_command)

    if mission_time > 60:
        drone.abort_mission()

    time.sleep(0.1)
