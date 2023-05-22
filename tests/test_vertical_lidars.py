import time
import sys
import numpy as np

"""
Code to test boolean behavior of vertical lidars, also to test the connection to the raspberry, tested in the drone
"""
sys.path.insert(0, '../sensors')
from tf_mini_vertical import VerticalLidarsDetection

vertical_lidars = VerticalLidarsDetection(lidar_address=[0x16, 0x17], lidar_position=[0, 1])
"print(vertical_lidars.get_down_lidar()._address)"

for s in range(200):
    if vertical_lidars.get_up_lidar().lidar_reading():
        print("the up distance is : ")
        vertical_lidars.read_up_distance()
        print(vertical_lidars.get_up_distance())

    if vertical_lidars.get_down_lidar().lidar_reading():
        print("the down distance is :")
        vertical_lidars.read_down_distance()
        print(vertical_lidars.get_down_distance())

    vertical_lidars.update_vertical_path()
    print("go_down : ")
    print(vertical_lidars._go_down)
    print("go_up : ")
    print(vertical_lidars._go_up)

    time.sleep(5)

