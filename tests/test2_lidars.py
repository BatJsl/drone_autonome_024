from tf_mini import TFMiniPlus
import time

list_lidars = [10, 11]
sensors = []


def test_lidar():
    Sensor10 = TFMiniPlus(0x10, 0)
    Sensor11 = TFMiniPlus(0x11, 0)
    while True:
        if Sensor10.lidar_reading():
            Sensor10.read_distance()
            print("sensor10 dist is :", Sensor10.get_distance())
        if Sensor11.lidar_reading():
            Sensor11.read_distance()
            print("sensor11 dist is :", Sensor11.get_distance())
        time.sleep(1)
    return 0


print(test_lidar())

print("test à vérifier")
