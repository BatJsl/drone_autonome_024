from tf_mini import TFMiniPlus
from enum import Enum
def tresh_lerp(tresh,LX,LY,DX,DY):
    fact = 2*tresh-(((LX/LY)-(1-tresh))/(2*tresh))
    DeltaX_r = -fact*DX
    DeltaY_r = -(1-fact)*DY
    return DeltaX_r, DeltaY_r
def filter_zeros(value):
    if value == 0 :
        return 1000
    else :
        return value
class State(Enum):
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
        self._lidar_number = len(tfminis)
        self.distances = [0,0,0,0]
        self.state = State.STOP


    def lidar_reading(self):
        for tfmini in self.tfminis:
            if tfmini.lidar_reading():
                return True
        return False

    def read_distances(self):
        for i in range(self._lidar_number):
            sensor = self.tfminis[i]
            sensor.read_distance()

    def get_distances(self):
        self.distances = []
        for tfmini in self.tfminis:
            self.distances.append(tfmini.get_distance())
        print("in get distances", self.distances)

    def show_distances_3sensors(self):
        print(len(self.distances))
        print("Left distance :", self.distances[0],'mm',"Front distance :", self.distances[1],'mm',"Right distance :", self.distances[2],'mm')

    def corridor_detected(self):
        return self.distances != [] and sum(self.distances) > 0


    def generate_instructions_4sensors(self):
        """
        Changes the state of the drone according to the lidar readings
        """
        front_distance = filter_zeros(self.distances[1])
        left_distance = filter_zeros(self.distances[0])
        right_distance = filter_zeros(self.distances[2])
        factor = 1
        if front_distance < 2 * (left_distance + right_distance):
            print("in generate instructions : turn")
            self.state = State.TURN
        else:
            if left_distance / right_distance > 1.2:
                self.state = State.LEFT
                factor = min((left_distance / right_distance)-1.2,1)
                print("in generate instructions : left")

            elif right_distance / left_distance > 1.2:
                self.state = State.RIGHT
                factor = min((right_distance / left_distance) - 1.2, 1)
                print("in generate instructions : right")
            else :
                self.state = State.FORWARD
                print("in generate instructions : front")
        return factor

    def generate_instructions_4sensors_wip(self,tresh):
        """
        Changes the state of the drone according to the lidar readings
        """
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

    def update_path(self, corridor_detected):
        if corridor_detected:
            factor = self.generate_instructions_4sensors()
        else :
            factor  = 1
            print("no corridor detected")
        return factor