from tf_mini import TFMiniPlus

def tresh_lerp(tresh,LX,LY,DX,DY):
    fact = 2*tresh-(((LX/LY)-(1-tresh))/(2*tresh))
    DeltaX_r = -fact*DX
    DeltaY_r = -(1-fact)*DY
    return DeltaX_r, DeltaY_r

class State(enum.Enum):
    STOP = "stop"
    FORWARD = "forward"
    BACKWARD = "backward"
    LEFT = "left"
    RIGHT = "right"
    TURN = "turn"
    DIAG = "diagonal"

class DroneLidarSensors(object):
    def __init__(self, tfminis):
        self.tfminis = tfminis
        self.distances = []
        self.state = State.STOP

    def get_distances(self):
        if True :
            self.distances = []
            for tfmini in self.tfminis:
                tfmini.read_distance()

                self.distances.append(tfmini.get_distance())

    def show_distances_3sensors(self):
        print(len(self.distances))
        print("Left distance :", self.distances[0],'mm',"Front distance :", self.distances[1],'mm',"Right distance :", self.distances[2],'mm')

    def generate_instructions_3sensors(self):
        front_distance = max(1,self.distances[1])
        left_distance = max(1,self.distances[0])
        right_distance = max(1,self.distances[2])
        if front_distance < 2 * (left_distance + right_distance):
            self.state = State.TURN
        else:
            if max(left_distance / right_distance, right_distance / left_distance) > 1.2:
                if left_distance > right_distance:
                    self.state = State.LEFT
                else:
                    self.state = State.RIGHT
            else:
                self.state = State.FORWARD

    def generate_instructions_4sensors(self,tresh):
        front_distance = max(1,self.distances[1])
        back_distance = max(1,self.distances[3])
        left_distance = max(1,self.distances[0])
        right_distance = max(1,self.distances[2])

        DeltaX = (right_distance - left_distance) / 2

        DeltaY = (back_distance - front_distance) / 2

        LX = (right_distance + left_distance) / 2  # longueur totale selon la direction x
        LY = (back_distance + front_distance) / 2  # longueur totale selon la direction y
        if abs(1 - LX / LY) < tresh:

            DX = LX - left_distance
            DY = LY - front_distance

            DeltaX_r, DeltaY_r = tresh_lerp(tresh, LX, LY, DX, DY)
            self.state = State.DIAG
            print(DeltaX_r, DeltaY_r)

        elif LX > LY:
            if(DeltaY>0):
                self.state = State.BACKWARD
            else :
                self.state = State.FORWARD
        else:
            if(DeltaX>0):
                self.state = State.RIGHT
            else:
                self.state = State.LEFT

class DroneLidarSensors(object):
    """
    Class of lidar sensors
    Used to deal with multiple sensors on the drone
    """
    def __init__(self, lidar_address, lidar_angle, critical_distance_lidar=100):
        self._lidar_number = len(lidar_angle)  # Number of lidar sensors
        self._critical_distance_lidar = critical_distance_lidar
        # Initialize a list with all the lidar sensors
        self.lidar_sensors = self._init_lidar_sensors(lidar_address, lidar_angle)

    def _init_lidar_sensors(self, lidar_address, lidar_angle):
        """
        Initialize a list of lidar sensors with their address and angle
        """
        lidar_sensors = []  # List of lidar sensors
        if lidar_address is not None:
            index = dict(zip(lidar_address, lidar_angle))  # Dictionary of address and angle
            for address, angle in index.items():
                # Initialize a lidar
                lidar_sensors.append(TFMiniPlus(address, angle, self._critical_distance_lidar))
        return lidar_sensors


class ThreeLidarSensorsDetection(object):
    """
    Class specific to a detection using three lidar sensor
    """
    def __init__(self, lidar_address=None, lidar_angle=[0], critical_distance_lidar=100):
        # Initialize the three lidar sensors
        self._lidar_sensors = DroneLidarSensors(lidar_address, lidar_angle).lidar_sensors
        self._right_lidar = None
        self._left_lidar = None
        self._front_lidar = None
        # Sort the sensor depending on their angle
        self._sort_sensors()
        self._obstacle_detected_right = False
        self._obstacle_detected_left = False
        self.go_right = True
        self.go_left = True

    def _sort_sensors(self):
        """
        Function sorting the three sensors depending on their angle
        """
        for lidar in self._lidar_sensors:
            if lidar.angle == 0:
                lidar.name = "Front lidar"
                self._front_lidar = lidar
            elif lidar.angle == -90:
                lidar.name = "Left lidar"
                self._left_lidar = lidar
            elif lidar.angle == 90:
                lidar.name = "Right lidar"
                self._right_lidar = lidar

    # Functions to access the lidar
    def get_front_lidar(self):
        return self._front_lidar

    def get_right_lidar(self):
        return self._right_lidar

    def get_left_lidar(self):
        return self._left_lidar

    # Redefinition of functions using the front lidar
    def read_distance(self):
        return self._front_lidar.read_distance()

    def get_distance(self):
        return self._front_lidar.get_distance()

    def critical_distance_reached(self):
        return self._front_lidar.critical_distance_reached()

    def lidar_reading(self):
        return self._front_lidar.lidar_reading()

    # Specific functions for right and left lidar
    def read_right_distance(self):
        return self._right_lidar.read_distance()

    def read_left_distance(self):
        return self._left_lidar.read_distance()

    def obstacle_detected_right(self):
        return self._obstacle_detected_right

    def obstacle_detected_left(self):
        return self._obstacle_detected_left

    def update_path(self, obstacle_detected):
        """
        Function used to update the possible path for the drone
        Check if the drone can go left or right when it detects an obstacle in front of him
        """
        # Obstacle in front of the drone : check the right and left directions
        if obstacle_detected:
            if self._obstacle_detected_left:
                self.go_left = False
            if self._obstacle_detected_right:
                self.go_right = False
        # No obstacle in front of the drone : restore parameters value
        else:
            self.go_left = True
            self.go_right = True
