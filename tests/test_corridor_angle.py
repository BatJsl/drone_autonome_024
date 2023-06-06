# dronekit-sitl copter-3.3 --home=48.8411292,2.5879308,584,353
# mavproxy.exe --master tcp:127.0.0.1:5760 --out udp:127.0.0.1:14550 --out udp:127.0.0.1:14551
# mavproxy.py --master tcp:127.0.0.1:5760 --out udp:127.0.0.1:14550 --out udp:127.0.0.1:14551
# cd branch_corridor/projet_drone_024/tests
# python test_corridor_angle.py --connect udp:127.0.0.1:14551
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
from wall import WallObstacle

simulation = True

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
    x01 = -100.0
    y01 = 100.0
    length = 250.0
    angle1 = 0.0
    width_corridor = 200.0

    corridor1 = CorridorObstacle(x01, y01, length, angle1, width_corridor)
    walls1 = corridor1.walls_corridor()

    x02 = x01 + length
    y02 = y01 - width_corridor
    angle2 = angle1 + 90
    corridor2 = CorridorObstacle(x02, y02, length, angle2, width_corridor)

    walls2 = corridor2.walls_corridor()

    # wall3
    x3 = x01
    y3 = y01 + length
    angle3 = angle1
    wall3 = WallObstacle(x3, y3, width_corridor, angle3)

    # wall4
    x4 = x01
    y4 = y3 + width_corridor
    angle4 = angle3 + 90
    wall4 = WallObstacle(x4, y4, width_corridor, angle4)

    walls = [walls1, walls2, wall3, wall4]
else:
    drone = InspectionDrone(connection_string, baudrate=115200,
                            two_way_switches=[7, 8], three_way_switches=[5, 6, 8, 9, 10, 11, 12])
# Base velocity :

Speed = 1

drone.launch_mission()
# Simulation : arm and takeoff the drone
if simulation:
    drone.arm_and_takeoff(0.7)

while drone.mission_running():
    drone.update_time()  # update time since connexion and mission's start
    drone.update_switch_states()  # update the RC transmitter switch state
    if drone.do_lidar_reading():  # ask a reading every 20 ms
        if simulation:
            drone.update_detection(use_lidar=True, debug=True, walls=walls)  # distance measure
            drone.update_side_detection(debug=True, walls=walls)
        else:
            drone.update_detection(use_lidar=True, debug=True)  # distance measure
            drone.update_side_detection(use_lidar=True, debug=True)
    if drone.corridor_detected() and drone.is_in_auto_mode():  # obstacle detected in front of the drone IRL
        drone.set_guided_mode()
        drone.send_mavlink_stay_stationary()
    if drone.corridor_detected() and simulation and first_detection:  # obstacle detected in front of the drone in simulation
        print("Obstacle detected")
        drone.set_guided_mode()
        drone.send_mavlink_stay_stationary()
        first_detection = False
    if drone.corridor_detected() and drone.is_in_guided_mode():
        drone.lidar.update_path(drone.corridor_detected())
        if drone.lidar.go_left:  # no obstacle left
            drone.send_mavlink_go_left(0.5)
        elif drone.lidar.go_right:  # no obstacle right
            drone.send_mavlink_go_right(0.5)
    if not drone.corridor_detected() and drone.is_in_guided_mode()\
            and drone.time_since_last_obstacle_detected() > 3 and not simulation:  # obstacle avoided IRL
        drone.set_auto_mode()  # resume mission
        drone.lidar.update_path(drone.corridor_detected())
    if not drone.corridor_detected() and drone.is_in_guided_mode() \
            and drone.time_since_last_obstacle_detected() > 3 and simulation:  # obstacle avoided simulator
        first_detection = True  # resume mission
        drone.lidar.update_path(drone.corridor_detected())
    if not drone.corridor_detected() and simulation and first_detection:  # drone move forward in simulation
        drone.send_mavlink_go_forward(0.5)
    if drone.time_since_last_obstacle_detected() > 60:
        drone.abort_mission()
    time.sleep(0.1)

