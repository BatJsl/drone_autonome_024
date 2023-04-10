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

list_up_dist = list(range(250, 500, 1))
list_down_dist =list(range(500, 250, -1))

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

    if drone.vert_lidar.lidar_reading():
        drone.vert_lidar.read_up_distance()
        drone.vert_lidar.read_down_distance()

    if drone.is_in_auto_mode():
        drone.set_guided_mode()
        drone.send_mavlink_stay_stationary()

    drone.vert_lidar.update_vertical_path()

    if drone.vert_lidar._go_up:
        drone.send_ned_velocity(0, 0, 0.1)
    elif drone.vert_lidar._go_down:
        drone.send_ned_velocity(0, 0, -0.1)

    time.sleep(2)

    drone.set_auto_mode()

    if drone._start_time>70:
        drone.abort_mission()
time.sleep(1)




