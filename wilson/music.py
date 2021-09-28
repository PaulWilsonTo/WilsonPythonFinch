'''
  © Paul Wilson 2021
    Published under the Simple Public License:
    https://opensource.org/licenses/Simple-2.0
  For controlling BirdBrain Technologies Finch 2.0
    with Java and Python in online IDE like ReplIt
    see https://www.birdbraintechnologies.com/
'''
class Music():
  def __init__(self):
    self.list = []
  
  def addNote(self, midiNote, duration):
    self.list.append({
      "midiNote": midiNote, "duration": duration
    })
  
  def getList(self):
    return self.list
