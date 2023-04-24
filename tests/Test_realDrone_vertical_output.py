"""
Test the vertical output of the code in the drone environment using the raspberry pi Zero
"""

import sys
import time
sys.path.insert(0, '../drone')
sys.path.insert(0, '../sensors')
from tf_mini_vertical import VerticalLidarsDetection

vertical_lidars = VerticalLidarsDetection(lidar_address=[0x11, 0x12], lidar_position=[0, 1])
# 1 above, 0 below the drone

mission = True

while mission:
    for i in range(200):
        if vertical_lidars.get_up_lidar().lidar_reading():
            print("the up distance is : ")
            vertical_lidars.read_up_distance()
            print(vertical_lidars.get_up_distance())

        if vertical_lidars.get_down_lidar().lidar_reading():
            print("the down distance is :")
            vertical_lidars.read_down_distance()
            print(vertical_lidars.get_down_distance())

        vertical_lidars.update_vertical_path()

        if vertical_lidars._go_up:
            print("aller plus haut")

        elif vertical_lidars._go_down:
            print("aller plus bas")
        else:
            print("c'est le milieu")
        time.sleep(1)

    mission = False







