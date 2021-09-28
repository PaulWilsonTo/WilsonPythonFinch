'''
  © Paul Wilson 2021
    Published under the Simple Public License:
    https://opensource.org/licenses/Simple-2.0
  For controlling BirdBrain Technologies Finch 2.0
    with Java and Python in online IDE like ReplIt
    see https://www.birdbraintechnologies.com/
'''
class Message():
  def __init__(self, message):
    self.sourceId = message.get("sourceId")
    self.command = message.get("command", None)
    self.response = message.get("response", None)
  
  def toString(self):
    return "sourceId: " + str(self.sourceId) \
      + ", command: " + str(self.command) \
      + ", response: " + str(self.response)
