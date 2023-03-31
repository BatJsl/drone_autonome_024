import sys

sys.path.insert(0, '../drone')
sys.path.insert(0, '../obstacles')
from wall import WallObstacle
from corridor import CorridorObstacle


# Init obstacles
x0 = -1000
y0 = 1000
length = 2000
angle = 45
wall1 = WallObstacle(x0, y0, length, angle)
width_corridor = 300
corridor = CorridorObstacle(x0, y0, length, angle, width_corridor)
walls = corridor.walls_corridor()

# print(corridor.equation_of_corridors())

print(corridor.draw_corridor())
# print(walls)
