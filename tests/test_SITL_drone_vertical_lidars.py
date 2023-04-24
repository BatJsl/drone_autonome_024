# dronekit-sitl copter-3.3 --home=48.8411292,2.5879308,584,353
# mavproxy.exe --master tcp:127.0.0.1:5760 --out udp:127.0.0.1:14550 --out udp:127.0.0.1:14551
# python test_drone_vertical_lidars.py --connect udp:127.0.0.1:14551

"""
Test vertical movement with vertical lidars, simulation environment
"""

import sys
import time
import argparse

sys.path.insert(0, '../drone')
from virtual_drone_vertical_mov import VirtualDrone

simulation = True

parser = argparse.ArgumentParser(description='commands')
parser.add_argument('--connect')
args = parser.parse_args()

connection_string = args.connect

list_1 = list(range(250, 500, 1))
list_2 = list(range(500, 300, -1))
list_3 = list(range(300, 450, 1))
list_4 = list(range(450, 400, -1))
list_5 = list(range(400, 350, -1))
list_6 = list(range(350, 390, 1))
list_7 = list(range(390, 360, -1))

list_down_dist = list_1 + list_2 + list_3 + list_4 + list_5 + list_6 + list_7

list_1 = list(range(500, 250, -1))
list_2 = list(range(250, 450, 1))
list_3 = list(range(450, 300, -1))
list_4 = list(range(300, 350, 1))
list_5 = list(range(350, 400, 1))
list_6 = list(range(400, 360, -1))
list_7 = list(range(360, 390, 1))

list_up_dist = list_1 + list_2 + list_3 + list_4 + list_5 + list_6 + list_7

if connection_string is None:
    connection_string = '/dev/serial0'

if simulation:
    drone = VirtualDrone(connection_string=connection_string, baudrate=115200,
                         two_way_switches=[7, 8], three_way_switches=[5, 6, 8, 9, 10, 11, 12],
                         lidar_angle=[0, 90, -90], critical_distance_lidar=100,
                         list_up_distances=list_up_dist, list_down_distances=list_down_dist)

drone.launch_mission()
# Simulation : arm and takeoff the drone

if simulation:
    drone.arm_and_takeoff(2)

while drone.mission_running():
    drone.update_time()
    drone.update_switch_states()
    for i in range(len(list_down_dist)/10):
        count = i*10
        if drone.vert_lidar.lidar_reading():
            print("Doing vertical reading")
            drone.vert_lidar._distance_up = list_up_dist[count]
            print("distance_up")
            print(drone.vert_lidar._distance_up)
            drone.vert_lidar._distance_down = list_up_dist[count]
            print("distance_down")
            print(drone.vert_lidar._distance_down)

        if drone.is_in_auto_mode():
            print("Drone was in auto mode ")
            print("changing to guided mode ")
            drone.set_guided_mode()
            drone.send_mavlink_stay_stationary()
        drone.set_guided_mode()

        drone.vert_lidar.update_vertical_path()

        if drone.vert_lidar._go_up:
            print("going up")
            #drone.send_mavlink_go_left(0.05)
            drone.send_mavlink_go_up(0.15)
        elif drone.vert_lidar._go_down:
            print("going down")
            #drone.send_mavlink_go_right(0.05)
            drone.send_mavlink_go_down(0.15)

    # time.sleep(2)

    # drone.set_auto_mode()
    print("time")
    print(drone.time_since_mission_launch())
    if drone.time_since_mission_launch() > 300:
        drone.abort_mission()
    time.sleep(5)
time.sleep(10)
