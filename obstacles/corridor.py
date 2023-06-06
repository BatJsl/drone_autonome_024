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
        x_origin2 = self._width * np.cos(
            np.radians(self._angle) - np.pi / 2) + x0  # il faut convertir l'angle en radians
        y_origin2 = self._width * np.sin(np.radians(self._angle) - np.pi / 2) + y0  # pour trouver la position initiale
        return WallObstacle(x_origin2, y_origin2, self._dimension, self._angle)

    def walls_corridor(self):
        """
        returns a tuple of the two walls
        """
        return [self.get_first_wall(), self.get_second_wall()]

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

        wall1, wall2 = self.walls_corridor()
        x10, y10 = wall1._get_obstacle_origin()
        x11, y11 = x10 + np.cos(np.radians(self._angle)) * self._dimension, y10 + np.sin(np.radians(self._angle)) * self._dimension
        x20, y20 = wall2._get_obstacle_origin()
        x21, y21 = x20 + np.cos(np.radians(self._angle)) * self._dimension, y20 + np.sin(np.radians(self._angle)) * self._dimension

        n_step = 10

        if (self._angle == 90 or self._angle == -90):
            X1 = [x10 for k in range(n_step)]
            Y1 = [y10 + (k/n_step) * (y10 - y11) for k in range(n_step)]
            X2 = [x20 for k in range(n_step)]
            Y2 = Y1

        else:
            [[a1, b1], [a2, b2]] = self.equation_of_corridors()

            step1 = np.abs(x10 - x11) / n_step
            step2 = np.abs(x20 - x21) / n_step

            X1 = np.arange(np.min([x10, x11]), np.max([x11, x10]), step1)
            X2 = np.arange(np.min([x20, x21]), np.max([x21, x20]), step2)
            Y1 = a1 * X1 + b1
            Y2 = a2 * X2 + b2

        plt.plot(X1, Y1)
        plt.xlim(left=0, right=300)
        plt.ylim(bottom=-300, top=0)
        plt.plot(X2, Y2)
        plt.xlim(left=0, right=300)
        plt.ylim(bottom=-300, top=0)
        plt.grid()
        plt.show()
        return 0
