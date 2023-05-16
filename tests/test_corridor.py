# dronekit-sitl copter-3.3 --home=48.8411292,2.5879308,584,353
# mavproxy.exe --master tcp:127.0.0.1:5760 --out udp:127.0.0.1:14550 --out udp:127.0.0.1:14551
# mavproxy.py --master tcp:127.0.0.1:5760 --out udp:127.0.0.1:14550 --out udp:127.0.0.1:14551
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
from drone_sensors import State

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

else:
    drone = InspectionDrone(connection_string, baudrate=115200,
                            two_way_switches=[7, 8], three_way_switches=[5, 6, 8, 9, 10, 11, 12],
                            lidar_angle=[-90, 0, 90, 180], lidar_address=[0x12, 0x10, 0x11, 0x13])


# Init obstacles
x0 = -1000
y0 = 1000
length = 2000
angle = -45
width_corridor = 300

#Base velocity :

Speed = 1

corridor = CorridorObstacle(x0, y0, length, angle, width_corridor)
walls = corridor.walls_corridor()

drone.launch_mission()
# Simulation : arm and takeoff the drone
if simulation:
    drone.arm_and_takeoff(2)

while drone.mission_running():
    drone.update_time()  # update time since connexion and mission's start
    drone.update_switch_states()  # update the RC transmitter switch state
    if drone.do_lidar_reading():  # ask a reading every 20 ms
        if simulation:
            drone.update_detection(use_lidar=True, debug=False, walls=walls)  # distance measure
            print("detection updated")
        else:
            drone.update_detection(use_lidar=True, debug=True)  # distance measure
    if drone.corridor_detected() and simulation and first_detection:  # corridor detected in front of the drone in simulation
        print("Corridor detected")
        drone.set_guided_mode()
        drone.send_mavlink_stay_stationary()
        first_detection = False
    if drone.corridor_detected() and drone.is_in_guided_mode():
        drone.lidar.update_path(drone.corridor_detected())
        if drone.lidar.state == State.LEFT:  # strafe left
            drone.send_mavlink_go_left(Speed)
        elif drone.lidar.state == State.RIGHT:  # strafe right
            drone.send_mavlink_go_right(Speed)
        elif drone.lidar.state == State.FORWARD:  # go forward
            drone.send_mavlink_go_forward(Speed)
        elif drone.lidar.state == State.BACKWARD:  # go backward
            drone.send_mavlink_go_backward(Speed)
        elif drone.lidar.state == State.TURN:  # turn
            drone.send_mavlink_right_rotate(10)
        elif drone.lidar.state == State.STOP:  # stop
            drone.send_mavlink_stay_stationary()
    if not drone.corridor_detected() and drone.is_in_guided_mode()\
            and drone.time_since_last_corridor_detected() > 3 and not simulation:  # obstacle avoided IRL
        drone.send_mavlink_stay_stationary()
        drone.lidar.update_path(drone.corridor_detected())
    if not drone.corridor_detected() and drone.is_in_guided_mode() \
            and drone.time_since_last_corridor_detected() > 3 and simulation:  # obstacle avoided simulator
        first_detection = True  # resume mission
        drone.lidar.update_path(drone.corridor_detected())
    """
    if drone.time_since_last_corridor_detected() > 60:
        print("No corridor detected", drone.lidar.distances)
        drone.abort_mission()
    """
    time.sleep(0.1)

