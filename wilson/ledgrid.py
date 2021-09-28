'''
  © Paul Wilson 2021
    Published under the Simple Public License:
    https://opensource.org/licenses/Simple-2.0
  For controlling BirdBrain Technologies Finch 2.0
    with Java and Python in online IDE like ReplIt
    see https://www.birdbraintechnologies.com/
'''
class LedGrid():
  def __init__(self):
    self.list = [
      0, 0, 0, 0, 0,
      0, 0, 0, 0, 0,
      0, 0, 0, 0, 0,
      0, 0, 0, 0, 0,
      0, 0, 0, 0, 0
    ]
  
  def setLed(self, row, col, led = True):
    index = 5 * row + col
    self.list[index] = (led if 1 else 0)
  
  def getList(self):
    return self.list
