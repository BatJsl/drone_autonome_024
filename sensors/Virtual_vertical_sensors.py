from range_sensors import RangeSensor
import time
import numpy as np

class VirtualVerticalSensors(RangeSensor):
    """
    Class to create vertical store distance elements for the essays in SITL
    """
    def __init__(self, list_up_distances=None, list_down_distances=None):
        RangeSensor.__init__(self)
        self._distance_up = None
        self._distance_down = None
        self._go_up = False
        self._go_down = False
        self.list_up_distances = list_up_distances
        self.list_down_distances = list_down_distances
        # Ask a reading every 20 ms
        self._time_between_readings = 0.02

    def read_up_distance(self):
        self._distance_up = self.list_up_distances.pop(0)

    def read_down_distance(self):
        self._distance_down = self.list_down_distances.pop(0)

    def get_up_distance(self):
        return self._distance_up

    def get_down_distance(self):
        return self._distance_down

    def lidar_reading(self):
        """
        Check if the time since the last reading is superior to the default time between two readings
        """
        return self.time_since_last_reading() > self._time_between_readings

    def update_vertical_path(self):
        """
        Function used to update the vertical path. We want the drone to be steady if it is at 10cm of the middle at most
        """
        up_dis = self.get_up_distance()
        down_dis = self.get_down_distance()
        middle = np.abs(up_dis-down_dis)/2

        if up_dis > down_dis and np.abs(up_dis - middle) > 10:
            self._go_up = True
            self._go_down = False
        elif up_dis < down_dis and np.abs(down_dis - middle) > 10:
            self._go_down = True
            self._go_up = False
        else:
            self._go_down = False
            self._go_up = False
