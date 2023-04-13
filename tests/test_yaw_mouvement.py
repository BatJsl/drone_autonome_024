# dronekit-sitl copter-3.3 --home=48.8411292,2.5879308,584,353
# mavproxy.exe --master tcp:127.0.0.1:5760 --out udp:127.0.0.1:14550 --out udp:127.0.0.1:14551
# python test_yaw_mouvement.py --connect udp:127.0.0.1:14551

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

list_up_dist = list(range(250, 500, 5))
list_down_dist = list(range(500, 250, -5))

if connection_string is None:
    connection_string = '/dev/serial0'

if simulation:
    drone = VirtualDrone(connection_string=connection_string, baudrate=115200,
                         two_way_switches=[7, 8], three_way_switches=[5, 6, 8, 9, 10, 11, 12],
                         lidar_angle=[0, 90, -90], critical_distance_lidar=100,
                         list_up_distances=list_down_dist, list_down_distances=list_up_dist)

drone.launch_mission()
# Simulation : arm and takeoff the drone

if simulation:
    drone.arm_and_takeoff(2)

while drone.mission_running():
    drone.update_time()
    drone.update_switch_states()

    """if drone.vert_lidar.lidar_reading():
        print("Doing reading")
        drone.vert_lidar.read_up_distance()
        print("distance_up")
        print(drone.vert_lidar._distance_up)
        drone.vert_lidar.read_down_distance()
        print("distance_down")
        print(drone.vert_lidar._distance_down)

    if drone.is_in_auto_mode():
        print("Drone was in auto mode ")
        print("changing to guided mode ")
        drone.set_guided_mode()
        drone.send_mavlink_stay_stationary()
    drone.set_guided_mode()
    drone.vert_lidar.update_vertical_path()
"""
    for i in range (1,2):
        print("rotating CW")
        drone.send_mavlink_right_rotate(30)
        time.sleep(1)
        print("time")
    """elif drone.vert_lidar._go_down:
        print("rotating CCW")
        drone.send_mavlink_left_rotate(30)
        time.sleep(1)"""

    #time.sleep(2)

    #drone.set_auto_mode()

    print(drone.time_since_mission_launch())
    if drone.time_since_mission_launch() > 300:
        drone.abort_mission()
    time.sleep(5)
time.sleep(10)