import time
import sys
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
                        lidar_address=[0x10], lidar_angle=[0], lidar_vertical_address=[0x14, 0x15],
                        lidar_vertical_position=[0,1], critical_distance_lidar=200)

drone.launch_mission()

while drone.mission_running():
    drone.update_time()  # update time since connexion and mission's start
    drone.update_switch_states()
    #if drone.time_since_mission_launch() > 50:
    if not drone.is_in_guided_mode():
        drone.set_guided_mode()
    if drone.vertical_lidars.get_up_lidar().lidar_reading():
        drone.send_mavlink_stay_stationary()
        print("Doing vertical reading")
        drone.vertical_lidars.read_up_distance()
        print("distance_up")
        print(drone.vertical_lidars._distance_up)
        drone.vertical_lidars.read_down_distance()
        print("distance_down")
        print(drone.vertical_lidars._distance_down)

        drone.update_vertical_detection()

        if drone.vertical_lidars._go_up:
            print("going up")
            drone.send_mavlink_go_up(0.15)
        elif drone.vertical_lidars._go_down:
            print("going down")
            drone.send_mavlink_go_down(0.15)

    time.sleep(1)
    print("time")
    print(drone.time_since_mission_launch())
    if drone.time_since_mission_launch() > 300:
        drone.abort_mission()

"""
import time
import sys
sys.path.insert(0, '../drone')
from inspection_drone import InspectionDrone


# Connection between the Raspberry and the Pixhawk
drone = InspectionDrone('/dev/serial0', baudrate=115200,
                        two_way_switches=[7, 8], three_way_switches=[5, 6, 9, 10, 11, 12],
                        lidar_address=[0x10], lidar_angle=[0],
                        critical_distance_lidar=200)

# Access to parameters
for _ in range(10):
    print("Drone velocity :", drone.vehicle.velocity)
    time.sleep(1)

# Change mode
print("Actual mode:", drone.vehicle.mode)
drone.set_guided_mode()
print("New mode:", drone.vehicle.mode)"""