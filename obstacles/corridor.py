from wall import WallObstacle
import numpy as np
import matplotlib.pyplot as plt
class CorridorObstacle(WallObstacle):
    """
    Definition of a class for corridors, since this year's project is in corridors
    We take one wall and the corridor's length to create two parallel walls
    """

    def __init__(self, x_origin, y_origin, dimension, angle, width):
        WallObstacle.__init__(self, x_origin, y_origin, dimension, angle)
        self._width = width

    def _get_corridor_origin(self):
        """
        gives the origin of the first wall (given as argument)
        """
        return self._x_origin, self._y_origin

    def get_first_wall(self):
        """
        returns the first WallObstacle
        """
        return WallObstacle(self._x_origin, self._y_origin, self._dimension, self._angle)

    def get_second_wall(self):
        """
        returns the second wall as a WallObstacle
        """
        x0, y0 = self._get_corridor_origin()
        x_origin2 = self._width * np.cos(np.radians(self._angle)-np.pi/2) + x0           # il faut convertir l'angle en radians
        y_origin2 = self._width * np.sin(np.radians(self._angle)-np.pi/2) + y0            # pour trouver la position initiale
        return WallObstacle(x_origin2, y_origin2, self._dimension, self._angle)


    def walls_corridor(self):
        """
        returns a tuple of the two walls
        """
        walls_of_corridor = [self, self.get_second_wall()]
        return walls_of_corridor

    def equation_of_corridors(self):
        wall1 = self.get_first_wall()
        wall2 = self.get_second_wall()
        wall1_eq = wall1._obstacle_equation()
        wall2_eq = wall2._obstacle_equation()
        return wall1_eq, wall2_eq

    def draw_corridor(self):
        """
        draws the corridor on a plane
        """
        x0, y0 = self._get_corridor_origin()

        origin_of_system = [x0 - 10, y0]
        plt.plot()
        return 0