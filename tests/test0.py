import sys

sys.path.insert(0, '../drone')
sys.path.insert(0, '../obstacles')
from obstacles.wall import WallObstacle
from obstacles.corridor import CorridorObstacle


# Init obstacles
wall1 = WallObstacle(-1000, 1000, 2000, 0)
width_corridor = 30
corridor = CorridorObstacle(wall1, width_corridor)
walls = corridor.walls_corridor()

print(walls)
