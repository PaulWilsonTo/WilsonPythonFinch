'''
  © Paul Wilson 2021
    Published under the Simple Public License:
    https://opensource.org/licenses/Simple-2.0
  For controlling BirdBrain Technologies Finch 2.0
    with Java and Python in online IDE like ReplIt
    see https://www.birdbraintechnologies.com/
'''
from threading import Thread, Event, current_thread
from importlib import import_module
from wilson.internal.device import Device
from wilson.internal.status import Status
from wilson.internal.command import Command
from wilson.internal.common import debug

class Worker():
  workers = {}

  @staticmethod
  def getById(sourceId):
    debug("WORKER getById", sourceId)
    if sourceId in Worker.workers:
      return Worker.workers[sourceId]
    else:
      return None
  
  def __init__(self, sourceId, runModule):
    debug("WORKER init", sourceId)
    self.sourceId = sourceId
    self.runModule = runModule
    self.target = 0
    self.finches = {}
    self.command = None
    self.pending = None
    self.response = None
    self.queue = None
    self.event = None
    Worker.workers[sourceId] = self

    thread = Thread(target = self.__runMainCode)
    thread.sourceId = self.sourceId
    thread.start()
  
  @staticmethod
  def nextTarget():
    thread = current_thread()
    worker = Worker.getById(thread.sourceId)
    worker.target = worker.target + 1
    debug("WORKER nextTarget", worker.target)
    return worker.target
  
  def getFinchById(self, target):
    debug("WORKER getFinchById", self.sourceId, target)
    if target in self.finches:
      return self.finches.get(target)
    else:
      return None

  def __runMainCode(self):
    debug("WORKER runMainCode", self.sourceId)
    '''
    # This did not support functions defs!
    mainLines = None
    
    with open(self.runModule + ".py", "r") as mainFile:
      mainLines = mainFile.readlines()
    mainCode = "".join(mainLines)

    exec(mainCode)
    '''
    import_module(self.runModule)

    self.queueCommand(Command(0, "done", None))
    Worker.workers.pop(self.sourceId)
    debug("WORKER endMainCode", self.sourceId)
    exit()

  @staticmethod
  def queueCommand(command):
    debug("WORKER queueCommand", command.toString())
    thread = current_thread()
    worker = Worker.getById(thread.sourceId)
    worker.command = command
    worker.response = None
    
    worker.event = Event()
    worker.event.wait()
    worker.event = None

  def getCommand(self):
    debug("WORKER getCommand")
    command = self.command
    self.pending = command
    self.command = None
    return command
    
  def popCommand(self, message):
    debug("WORKER popCommand", message.toString(), self.pending.toString())
    if str(message.command) == str(self.pending.id):
      self.response = message.response
      self.pending = None
      if self.event is not None:
        self.event.set()

  @staticmethod
  def getResponse():
    debug("WORKER getResponse")
    thread = current_thread()
    worker = Worker.getById(thread.sourceId)
    response = worker.response
    worker.response = None
    return response

  @staticmethod
  def trackFinch(target, finch):
    thread = current_thread()
    debug("WORKER trackFinch", thread.sourceId, target)
    worker = Worker.getById(thread.sourceId)
    worker.finches[target] = finch

  @staticmethod
  def queueStatus(command):
    debug("WORKER queueStatus", command.toString())
    thread = current_thread()
    worker = Worker.getById(thread.sourceId)
    worker.queue = command
    
    worker.event = Event()
    worker.event.wait()
    worker.event = None

  def updateStatus(self, target, status):
    debug("WORKER updateStatus", self.sourceId, target, status)
    finch = self.finches.get(target)
    if finch is None: return
    
    finch.status = status
    command = self.queue
    if command is None: return
    
    if command.type in ["init","reset","calibrate"]:
      self.popStatus(command)
    elif command.type == "forward":
      leftStart = Status.getLeftTicks(finch.start)
      rightStart = Status.getRightTicks(finch.start)
      moveTicks = Device.getMoveTicks(command.params.get("distance"))
      isWorking = Status.getIsWorking(status)
      leftTicks = Status.getLeftTicks(status)
      rightTicks = Status.getRightTicks(status)
      leftMove = abs(leftTicks - leftStart)
      rightMove = abs(rightTicks - rightStart)
      moveActual = max(leftMove, rightMove)
      if not isWorking and (moveActual / moveTicks) > 0.99:
        self.popStatus(command)
    elif command.type == "right":
      leftStart = Status.getLeftTicks(finch.start)
      rightStart = Status.getRightTicks(finch.start)
      turnTicks = Device.getTurnTicks(command.params.get("angle"))
      isWorking = Status.getIsWorking(status)
      leftTicks = Status.getLeftTicks(status)
      rightTicks = Status.getRightTicks(status)
      leftTurn = abs(leftTicks - leftStart)
      rightTurn = abs(rightTicks - rightStart)
      turnActual = max(leftTurn, rightTurn)
      if not isWorking and (turnActual / turnTicks) > 0.99:
        self.popStatus(command)
    
  def popStatus(self, command):
    debug("WORKER popStatus", command.toString())
    self.queue = None
    if self.event is not None:
      self.event.set()
