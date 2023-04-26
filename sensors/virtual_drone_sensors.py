from virtual_tf_mini import VirtualTFMiniPlus
from drone_sensors import DroneLidarSensors


def _init_lidar_sensors(lidar_angle):
    """
    Initialize a list of lidar sensors with their address and angle
    """
    lidar_sensors = []  # List of lidar sensors
    if lidar_angle is not None:
        for angle in lidar_angle:
            # Initialize a lidar
            lidar_sensors.append(VirtualTFMiniPlus(angle))
    return lidar_sensors


class VirtualDroneLidarSensors(DroneLidarSensors):
    """
    Class of lidar sensors
    Used to deal with multiple sensors on the drone
    """
    def __init__(self, lidar_angle):
        DroneLidarSensors.__init__(_init_lidar_sensors(lidar_angle))


    def read_distances(self, drone_x, drone_y, drone_angle, walls):
        for i in range(self._lidar_number):
            sensor = self.lidar_sensors[i]
            sensor_angle = sensor.angle
            sensor.read_distance(drone_x, drone_y, (drone_angle - sensor_angle) % 360, walls)
