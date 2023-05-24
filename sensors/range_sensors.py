import time
from filter import Tresh_filter

# -------- Parent range sensor class ---------
DEFAULT_CRITICAL_DISTANCE = 100
Filter = Tresh_filter(999, 1)
class RangeSensor(object):
    """
    Class that defines a general range sensor.
    It cannot read data because this function is specific to each sensor.
    Thus this class cannot be used by itself but is very useful for the lidar and sonar child classes
    """
    def __init__(self):
        self.name = "Range sensor"
        self._range = 999  # range : last distance read by sensor
        self._start_time = time.time()  # stores the time at which the object was created (in ms)
        self.time_log = [time.time() - self._start_time]  # stores the time the range was stored in the log (in ms)
        self.log = [0]  # stores range values for visualization
        self._time_between_readings = 20

    def get_distance(self):
        """Returns the last distance read by the sensor"""
        return self._range

    def set_distance(self, distance_value):
        """Modifies the range value stored by the object.
        In the meantime, it stores this value and the time it was written in a list"""
        self._range = distance_value
        #self._range = Filter.update(self._range, distance_value)
        self.log.append(distance_value)
        self.time_log.append(time.time() - self._start_time)

    def time_since_last_reading(self):
        return time.time()-self._start_time-self.time_log[-1]

    def lidar_reading(self):
        """
        Check if the time since the last reading is superior to the fixed time between two readings
        """
        return self.time_since_last_reading() > self._time_between_readings