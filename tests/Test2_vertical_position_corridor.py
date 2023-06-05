# dronekit-sitl copter-3.3 --home=48.8411292,2.5879308,584,353
# mavproxy.exe --master tcp:127.0.0.1:5760 --out udp:127.0.0.1:14550 --out udp:127.0.0.1:14551
# python test_avoidance.py --connect udp:127.0.0.1:14551
"""
Test vertical positionning with vertical lidars in real Drone
"""

import sys
import time
import argparse

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

drone.launch_mission()

initial_poshold_mode = False
print("while cycle")
while not initial_poshold_mode:
    print(drone.get_last_flight_mode())
    if drone.is_in_poshold_mode():
        initial_poshold_mode = True
    time.sleep(0.2)
print("Sleep time 6 seg")
time.sleep(6)

while drone.mission_running():
    drone.update_time()  # update time since connexion and mission's start
    drone.update_switch_states()  # update the RC transmitter switch state
    if drone.vertical_lidars.get_up_lidar().lidar_reading():
        drone.vertical_lidars.update_vertical_path_corridor()

    if (drone.vertical_lidars._go_up or drone.vertical_lidars._go_down ) and drone.is_in_poshold_mode():
        print("changed to guided mode")
        drone.set_guided_mode()
        drone.send_mavlink_stay_stationary()

    if (drone.vertical_lidars._go_up or drone.vertical_lidars._go_down ) and drone.is_in_guided_mode():
        if drone.vertical_lidars._go_up:
            drone.send_mavlink_go_up(0.10)
            print("go up")
        elif drone.vertical_lidars._go_down:
            drone.send_mavlink_go_down(0.10)
            print("go down")
    if not drone.vertical_lidars.update_vertical_path_corridor() and drone.is_in_guided_mode() and \
            drone.time_since_guided_mode() >3:
#Ajouter une condition de temps, pour pas changer inmediatement
#and drone.time_since_last_obstacle_detected() > 3:  # obstacle avoided IRL
        print("changed to auto mode")
        drone.set_poshold_mode()  # resume mission
    if drone.time_since_last_obstacle_detected() > 60:
        drone.abort_mission()

    time.sleep(0.1)