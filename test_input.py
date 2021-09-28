'''
  © Paul Wilson 2021
    Published under the Simple Public License:
    https://opensource.org/licenses/Simple-2.0
  For controlling BirdBrain Technologies Finch 2.0
    with Java and Python in online IDE like ReplIt
    see https://www.birdbraintechnologies.com/
'''
from wilson import Finch

Finch.print("Control by Keyboard Input")
Finch.print("Enter for Forward, Q for Quit,")
Finch.print("L for Left, or R for Right")

finch = Finch()
while True:
  finch.runMotors(5, 5)
  command = Finch.input("Enter, L, R, or Q")
  if command.upper() == "L":
    finch.stopAll()
    finch.left(45)
  elif command.upper() == "R":
    finch.stopAll()
    finch.right(45)
  elif command.upper() == "Q":
    finch.stopAll()
    break
