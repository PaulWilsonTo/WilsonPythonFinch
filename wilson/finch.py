'''
  © Paul Wilson 2021
    Published under the Simple Public License:
    https://opensource.org/licenses/Simple-2.0
  For controlling BirdBrain Technologies Finch 2.0
    with Java and Python in online IDE like ReplIt
    see https://www.birdbraintechnologies.com/
'''
from wilson.internal.device import Device
from wilson.internal.command import Command
from wilson.internal.worker import Worker
from wilson.internal.common import debug
from wilson.music import Music
from wilson.sensor import Sensor
import time

class Finch():
  def __init__(self, prompt = "Connect Finch", initX = 0, initY = 0):
    self.__target = Worker.nextTarget()
    debug("FINCH init", prompt, self.__target)
    params = {
      "prompt": prompt, "initX": initX, "initY": initY
    }
    command = Command(self.__target, "init", params)
    Worker.queueCommand(command)

    response = Worker.getResponse()
    self.__device = response.get("device")
    self.__name = response.get("name")
    self.__version = response.get("version")

    self.__speed = 5.0
    self.__beakRGB = [0, 0, 0]
    self.__tail1RGB = [0, 0, 0]
    self.__tail2RGB = [0, 0, 0]
    self.__tail3RGB = [0, 0, 0]
    self.__tail4RGB = [0, 0, 0]

    Worker.trackFinch(self.__target, self)
    Worker.queueStatus(command)
    self.resetTicks()
  
  def getTarget(self):
    return self.__target
  
  def getDevice(self):
    return self.__device
  
  def getName(self):
    return self.__name
  
  def getVersion(self):
    return self.__version
  
  def speed(self, factor = None):
    debug("FINCH speed", self.__target, factor)
    if factor is not None:
      self.__speed = max(1, min(10, factor))
    else:
      return self.__speed
  
  def stopAll(self):
    debug("FINCH stopAll", self.__target)
    cmdBytes = Device.getStopAllBytes()
    params = {
      "bytes": cmdBytes
    }
    command = Command(self.__target, "stop", params)
    Worker.queueCommand(command)

  def forward(self, distance):
    debug("FINCH forward", self.__target, distance)
    self.start = self.status
    cmdBytes = Device.getForwardBytes(distance, self.__speed)
    params = {
      "bytes": cmdBytes, "distance": distance, "speed": self.__speed
    }
    command = Command(self.__target, "forward", params)
    Worker.queueCommand(command)
    Worker.queueStatus(command)

  def backward(self, distance):
    self.forward(-distance)
  
  def right(self, angle):
    debug("FINCH right", self.__target, angle)
    self.start = self.status
    cmdBytes = Device.getRightBytes(angle, self.__speed)
    params = {
      "bytes": cmdBytes, "angle": angle, "speed": self.__speed
    }
    command = Command(self.__target, "right", params)
    Worker.queueCommand(command)
    Worker.queueStatus(command)
  
  def left(self, angle):
    self.right(-angle)

  def runMotors(self, leftSpeed, rightSpeed):
    debug("FINCH runMotors", self.__target, leftSpeed, rightSpeed)
    leftFactor = max(-10, min(10, leftSpeed))
    rightFactor = max(-10, min(10, rightSpeed))
    cmdBytes = Device.getRunMotorsBytes(leftFactor, rightFactor)
    params = {
      "bytes": cmdBytes, "left": leftFactor, "right": rightFactor
    }
    command = Command(self.__target, "motors", params)
    Worker.queueCommand(command)
  
  def getSensors(self):
    return Sensor(self.status, self.__version)
  
  def beakColor(self, red, green, blue):
    debug("FINCH beakColor", self.__target, red, green, blue)
    self.__setLight(-1, red, green, blue)
    self.__setLights()
  
  def tailColor(self, index, red, green, blue):
    debug("FINCH tailColor", self.__target, index, red, green, blue)
    self.__setLight(index, red, green, blue)
    self.__setLights()
  
  def __setLight(self, index, red, green, blue):
    if index == 1: self.__tail1RGB = [red, green, blue]
    elif index == 2: self.__tail2RGB = [red, green, blue]
    elif index == 3: self.__tail3RGB = [red, green, blue]
    elif index == 4: self.__tail4RGB = [red, green, blue]
    elif index == -1: self.__beakRGB = [red, green, blue]
    elif index == 0:
      for light in [1, 2, 3, 4]:
        self.__setLight(light, red, green, blue)
    else:
      for light in [-1, 1, 2, 3, 4]:
        self.__setLight(light, red, green, blue)
  
  def __setLights(self):
    cmdBytes = Device.getLightBytes(self.__beakRGB,
      self.__tail1RGB, self.__tail2RGB,
      self.__tail3RGB, self.__tail4RGB)
    params = {
      "bytes": cmdBytes, "beak": self.__beakRGB,
      "tail1": self.__tail1RGB, "tail2": self.__tail2RGB,
      "tail3": self.__tail3RGB, "tail4": self.__tail4RGB
    }
    command = Command(self.__target, "lights", params)
    Worker.queueCommand(command)

  def flashLeds(self, phrase):
    debug("FINCH flashLeds", self.__target, phrase)
    cmdBytes = Device.getLedFlashBytes(phrase)
    params = {
      "bytes": cmdBytes, "phrase": phrase
    }
    command = Command(self.__target, "flash", params)
    Worker.queueCommand(command)
  
  def customLeds(self, ledGrid):
    debug("FINCH customLeds", self.__target, ledGrid)
    cmdBytes = Device.getLedGridBytes(ledGrid)
    params = {
      "bytes": cmdBytes, "ledGrid": ledGrid.getList()
    }
    command = Command(self.__target, "leds", params)
    Worker.queueCommand(command)

  def playSound(self, midiNote, duration):
    debug("FINCH playSound", self.__target, midiNote, duration)
    music = Music()
    music.addNote(midiNote, duration)
    self.playMusic(music)
  
  def playMusic(self, music):
    debug("FINCH playMusic", self.__target, music)
    cmdBytes = Device.getMusicBytes(music)
    params = {
      "bytes": cmdBytes, "music": music.getList()
    }
    command = Command(self.__target, "sound", params)
    Worker.queueCommand(command)
  
  def resetTicks(self):
    debug("FINCH resetTicks", self.__target)
    cmdBytes = Device.getResetTicksBytes()
    params = {
      "bytes": cmdBytes
    }
    command = Command(self.__target, "reset", params)
    Worker.queueCommand(command)
    Worker.queueStatus(command)
  
  def calibrate(self):
    debug("FINCH calibrate", self.__target)
    cmdBytes = Device.getCalibrationBytes()
    params = {
      "bytes": cmdBytes
    }
    command = Command(self.__target, "calibrate", params)
    Worker.queueCommand(command)
    Worker.queueStatus(command)

  @staticmethod
  def input(prompt):
    debug("FINCH input", prompt)
    params = {
      "prompt": prompt
    }
    command = Command(0, "input", params)
    Worker.queueCommand(command)
    response = Worker.getResponse()
    return response.get("input")

  @staticmethod
  def print(*message):
    debug("FINCH print", message)
    params = {
      "message": message
    }
    command = Command(0, "print", params)
    Worker.queueCommand(command)

  @staticmethod
  def debug(*message):
    debug("FINCH debug", message)
    params = {
      "message": message
    }
    command = Command(0, "debug", params)
    Worker.queueCommand(command)

  @staticmethod
  def sleep(milliseconds):
    debug("FINCH sleep", milliseconds)
    time.sleep(milliseconds / 1000)
