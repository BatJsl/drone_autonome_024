# dronekit-sitl copter-3.3 --home=48.8411292,2.5879308,584,353
# mavproxy.exe --master tcp:127.0.0.1:5760 --out udp:127.0.0.1:14550 --out udp:127.0.0.1:14551
# mavproxy.py --master tcp:127.0.0.1:5760 --out udp:127.0.0.1:14550 --out udp:127.0.0.1:14551
# cd branch_corridor/projet_drone_024/tests
# python test_corridor.py --connect udp:127.0.0.1:14551
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
    x0 = -1000
    y0 = 1000
    length = 20000
    angle = -45
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

while drone.mission_running():
    drone.update_time()  # update time since connexion and mission's start
    drone.update_switch_states()  # update the RC transmitter switch state
    if drone.do_lidar_reading():  # ask a reading every 20 ms
        if simulation:
            drone.update_detection(use_lidar=True, debug=False, walls=walls)  # distance measure
        else:
            drone.update_detection(use_lidar=True, debug=True)  # distance measure
    if drone.is_in_guided_mode() or True:
        drone.lidar.update_path(drone.corridor_detected())
        drone.choose_direction(Speed)
        print("in test corridor", drone.lidar.state)
    if not drone.corridor_detected() and drone.is_in_guided_mode()\
            and drone.time_since_last_corridor_detected() > 3 and not simulation:  # no corridor found IRL
        drone.send_mavlink_stay_stationary()
        drone.lidar.update_path(drone.corridor_detected())
    if not drone.corridor_detected() and drone.is_in_guided_mode() \
            and drone.time_since_last_corridor_detected() > 3 and simulation:  # no corridor found simulator
        first_detection = True  # resume mission
    time.sleep(0.1)

