'''
  © Paul Wilson 2021
    Published under the Simple Public License:
    https://opensource.org/licenses/Simple-2.0
  For controlling BirdBrain Technologies Finch 2.0
    with Java and Python in online IDE like ReplIt
    see https://www.birdbraintechnologies.com/
'''
from wilson import Finch

finch = Finch()
Finch.print("Target: " + str(finch.getTarget()))
Finch.print("Device: " + finch.getDevice())
Finch.print("Name: " + finch.getName())
Finch.print("Version: " + str(finch.getVersion()))
