"""
Test flying in a corridor avoidance with four lidar sensors
Version for simulator (simulation = True) and reality (simulation = False)
"""
import time
import sys
import argparse
sys.path.insert(0, '../drone')
sys.path.insert(0, '../obstacles')
from virtual_drone import VirtualDrone
from inspection_drone import InspectionDrone
from corridor import CorridorObstacle


simulation = False

parser = argparse.ArgumentParser(description='commands')
parser.add_argument('--connect')
args = parser.parse_args()

connection_string = args.connect

if connection_string is None:
    connection_string = '/dev/serial0'

if simulation:
    drone = VirtualDrone(connection_string=connection_string, baudrate=115200,
                         two_way_switches=[7, 8], three_way_switches=[5, 6, 8, 9, 10, 11, 12],
                         lidar_angle=[-90, 0, 90, 180])
    first_detection = True
    # Init obstacles
    x0 = -100
    y0 = 100
    length = 20000
    angle = 0
    width_corridor = 300

    corridor = CorridorObstacle(x0, y0, length, angle, width_corridor)
    walls = corridor.walls_corridor()

else:
    drone = InspectionDrone(connection_string, baudrate=115200,
                            two_way_switches=[7, 8], three_way_switches=[5, 6, 8, 9, 10, 11, 12])




#Base velocity :

Speed = .1



drone.launch_mission()
# Simulation : arm and takeoff the drone
if simulation:
    drone.arm_and_takeoff(0.7)

print("begin sleep")
time.sleep(10)
drone.set_guided_mode()
print("end sleep")

while drone.mission_running():
    drone.update_time()  # update time since connexion and mission's start
    drone.update_switch_states()  # update the RC transmitter switch state
    if drone.is_in_guided_mode() or True:
        drone.send_mavlink_right_rotate(90)
    time.sleep(3)
    print('time')