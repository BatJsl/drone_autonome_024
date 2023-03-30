import sys

sys.path.insert(0, '../drone')
sys.path.insert(0, '../obstacles')
from wall import WallObstacle
from corridor import CorridorObstacle


# Init obstacles
x0 = -1000
y0 = 1000
length = 2000
angle = 0
wall1 = WallObstacle(x0, y0, length, angle)
width_corridor = 30
corridor = CorridorObstacle(x0, y0, length, angle, width_corridor)
walls = corridor.walls_corridor()

print(wall1._obstacle_equation())

# print(walls)
