from tf_mini import TFMiniPlus
import numpy as np


class DroneVerticalSensors(object):
    """
    Class to define vertical sensors in the Drone
    Also to interact and obtain the measures from them.
    lidar position is seen like 1 if is above the drone
    0 if is below the drone
    """

    def __init__(self, lidar_address, lidar_position, critical_distance_lidar=100):
        self._critical_distance_lidar = critical_distance_lidar
        # Initialize a list with vertical lidar sensors
        self.lidar_v_sensors = self._init_lidar_v_sensors(lidar_address, lidar_position)

    def _init_lidar_v_sensors(self, lidar_address, lidar_position):
        """
        Initialize a list of class tfmini sensors for vertical position
        """
        lidar_v_sensor = []  # List of vertical sensors
        if lidar_address is not None:
            index = dict(zip(lidar_address, lidar_position))  # Dictionary of vertical Lidars
            for address, position in index.items():
                lidar_v_sensor.append(TFMiniPlus(address, [0], position, self._critical_distance_lidar))
        return lidar_v_sensor


class VerticalLidarsDetection(object):
    """
    Class to organize and identify the vertical lidars
    """

    def __init__(self, lidar_address, lidar_position, critical_distance_lidar=100):
        self._lidar_sensors = DroneVerticalSensors(lidar_address, lidar_position,
                                                   critical_distance_lidar).lidar_v_sensors
        self._up_lidar = None
        self._down_lidar = None
        self._distance_up = None
        self._distance_down = None
        self._go_up = False
        self._go_down = False
        self._obstacle_detected_up = False
        self._obstacle_detected_down = False

        self._identify_sensors()

    def _identify_sensors(self):
        """
        Function to organize the vertical lidars
        """
        for lidar in self._lidar_sensors:
            if lidar.v_position == 1:
                lidar.name = "Up lidar"
                self._up_lidar = lidar
            else:
                lidar.name = "Down lidar"
                self._down_lidar = lidar

    # Functions to access the different lidars
    def get_up_lidar(self):
        return self._up_lidar

    def get_down_lidar(self):
        return self._down_lidar

    # Functions to obtain the distances measure by the lidars

    def read_up_distance(self):
        self.get_up_lidar().read_distance()

    def get_up_distance(self):
        self._distance_up = self.get_up_lidar().get_distance()
        return self._distance_up

    def read_down_distance(self):
        self.get_down_lidar().read_distance()

    def get_down_distance(self):
        self._distance_down = self.get_down_lidar().get_distance()
        return self._distance_down

    # Functions to get data of obstacle and command of up or down

    def obstacle_detected_up(self):
        return self._obstacle_detected_up

    def obstacle_detected_down(self):
        return self._obstacle_detected_down

    # Function to send the direction to go to the drone
    def update_vertical_path_corridor(self):
        """
        Function used to update the vertical path in a corridor
        """
        self.read_up_distance()
        self.read_down_distance()
        up_dis = self.get_up_distance()
        down_dis = self.get_down_distance()
        print("up distance")
        print(up_dis)
        print("down distance")
        print(down_dis)

        if up_dis == 0 or down_dis == 0:
            print("no floor or roof")
            self._go_down = False
            self._go_up = False
        else:
            middle = (np.abs(self.get_up_distance() + self.get_down_distance()) / 2)
            if up_dis > down_dis and np.abs(up_dis - middle) > 10:
                self._go_up = True
                self._go_down = False
            elif up_dis < down_dis and np.abs(down_dis - middle) > 10:
                self._go_down = True
                self._go_up = False
            else:
                self._go_down = False
                self._go_up = False
                return False

    def update_vertical_path_obstacle(self, vertical_obstacle_detected):
        """
        Function used to update the vertical path if there's
        an obstacle(ceiling or floor closer than distance critique)
        """
        if vertical_obstacle_detected:
            if self._obstacle_detected_up:
                self._go_up = False
                self._go_down = True
            if self._obstacle_detected_down:
                self._go_down = False
                self._go_up = True
        else:
            self._go_down = False
            self._go_up = False
