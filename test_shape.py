'''
  © Paul Wilson 2021
    Published under the Simple Public License:
    https://opensource.org/licenses/Simple-2.0
  For controlling BirdBrain Technologies Finch 2.0
    with Java and Python in online IDE like ReplIt
    see https://www.birdbraintechnologies.com/
'''
from wilson import Finch

sides = int(Finch.input("Number of sides?"))
distance = float(Finch.input("Length of sides?"))
speed = float(Finch.input("Speed (1-10)?"))

finch = Finch()
finch.speed(speed)
for side in range(sides):
  finch.forward(distance)
  finch.right(360 / sides)
