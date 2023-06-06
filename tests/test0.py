import sys

sys.path.insert(0, '../drone')
sys.path.insert(0, '../obstacles')
from wall import WallObstacle
from corridor import CorridorObstacle

# Init obstacles
x01 = -100
y01 = 100
length = 250
angle1 = 0
width_corridor = 200

corridor1 = CorridorObstacle(x01, y01, length, angle1, width_corridor)
walls1 = corridor1.walls_corridor()

x02 = x01 + length
y02 = y01 - width_corridor
angle2 = angle1 + 90
corridor2 = CorridorObstacle(x02, y02, length, angle2, width_corridor)

walls2 = corridor2.walls_corridor()

# wall3
x3 = x01
y3 = y01 + length
angle3 = angle1
wall3 = WallObstacle(x3, y3, width_corridor, angle3)

# wall4
x4 = x01
y4 = y3 + width_corridor
angle4 = angle3 + 90
wall4 = WallObstacle(x4, y4, width_corridor, angle4)


print(corridor2.draw_corridor(), corridor1.draw_corridor())
walls = [walls1, walls2]

