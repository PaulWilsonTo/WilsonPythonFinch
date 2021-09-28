'''
  © Paul Wilson 2021
    Published under the Simple Public License:
    https://opensource.org/licenses/Simple-2.0
  For controlling BirdBrain Technologies Finch 2.0
    with Java and Python in online IDE like ReplIt
    see https://www.birdbraintechnologies.com/
'''
import uuid
import json

class Command():
  def __init__(self, target, type, params):
    self.id = uuid.uuid4()
    self.target = target
    self.type = type
    self.params = params

  def toJson(self):
    return json.dumps({
      "id": str(self.id),
      "target": int(self.target),
      "type": self.type,
      "params": self.params
    })
  
  def toString(self):
    return "id: " + str(self.id) \
      + ", target: " + str(self.target) \
      + ", type: " + str(self.type) \
      + ", params: " + str(self.params)
