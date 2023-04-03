from tf_mini import TFMiniPlus


class DroneVerticalSensors(object):
    """
    Class to define vertical sensors in the Drone
    Also to interact and obtain the measures from them.
    lidar position is seen like 1 if is above the drone
    0 if is below the drone
    """

    def __init__(self, lidar_address, lidar_position, critical_distance_lidar = 100):
        self._critical_distance_lidar = critical_distance_lidar
        # Initialize a list with vertical lidar sensors
        self.lidar_v_sensors = self._init_lidar_v_sensors(lidar_address, lidar_position)


    def _init_lidar_v_sensors(self, lidar_address, lidar_position):
        """
        Initialize a list of class tfmini sensors for vertical position
        """
        lidar_v_sensor = [] # List of vertical sensors
        if lidar_address is not None:
            index = dict(zip(lidar_address, lidar_position) # Dictionary of vertical lidars
            for address, position in index.items():
                lidar_v_sensor.append(TFMiniPlus(address, v_position=position, self._critical_distance_lidar))
        return lidar_v_sensor

class VerticalLidarsDetection(object):
    """
    Class to organize and identify the vertical lidars
    """

    def __init__(self,lidar_address, lidar_position, critical_distance_lidar = 100):
        self._lidar_sensors = DroneVerticalSensors(lidar_address, lidar_position, critical_distance_lidar = 100).lidar_v_sensors
        self._up_lidar = None
        self._down_lidar = None
        self._distance_up = None
        self._distance_down = None
        self._go_up = False
        self._go_down = False

        self._identify_sensors()

    def _identify_sensors(self):
        """
        Function to organize the vertical lidars
        """
