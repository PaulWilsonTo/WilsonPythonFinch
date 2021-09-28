'''
  © Paul Wilson 2021
    Published under the Simple Public License:
    https://opensource.org/licenses/Simple-2.0
  For controlling BirdBrain Technologies Finch 2.0
    with Java and Python in online IDE like ReplIt
    see https://www.birdbraintechnologies.com/
'''
from wilson import Finch

Finch.print("Control by Shining Light")
Finch.print("Shine on Left or Right Side")

finch = Finch()
while True:
  finch.runMotors(2, 2)
  sensors = finch.getSensors()
  if sensors.leftLight() >= 10:
    finch.stopAll()
    finch.left(45)
  elif sensors.rightLight() >= 10:
    finch.stopAll()
    finch.right(45)
  elif sensors.wallDistance() < 2:
    finch.stopAll()
    break
