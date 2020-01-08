# This is a NetworkTables server (eg, the robot or simulator side).
#
#  ip 127.0.0.1
#

from networktables import  NetworkTables
import time
# start a local version of Network Tables
NetworkTables.initialize()
sd = NetworkTables.getTable("SmartDashboard")

i = 0
while True:
    sd.putNumber("robotTime", i)
    time.sleep(5)
    i += 1
    print(i)