'''
  © Paul Wilson 2021
    Published under the Simple Public License:
    https://opensource.org/licenses/Simple-2.0
  For controlling BirdBrain Technologies Finch 2.0
    with Java and Python in online IDE like ReplIt
    see https://www.birdbraintechnologies.com/
'''
import math

class Status():
  def __init__(self, status):
    self.sourceId = status.get("sourceId")
    self.target = status.get("target", 0)
    self.status = status.get("status", None)
  
  def toString(self):
    return "sourceId: " + str(self.sourceId) \
      + ", target: " + str(self.target) \
      + ", status: " + str(self.status)

  @staticmethod
  def getIsWorking(status):
    return (status.get("4") // 128 == 1)

  @staticmethod
  def getLeftTicks(status):
    return Status.combineBytes(status.get("9"), status.get("8"), status.get("7"))

  @staticmethod
  def getRightTicks(status):
    return Status.combineBytes(status.get("12"), status.get("11"), status.get("10"))

  @staticmethod
  def getDistance(status, version):
    if version == 1: return Status.combineBytes(status.get("1"), status.get("0"))
    elif version == 2: return status.get("1")
    else: return 0

  @staticmethod
  def getLeftLine(status):
    return status.get("4") % 128

  @staticmethod
  def getRightLine(status):
    return status.get("5")

  @staticmethod
  def getLeftLight(status):
    return status.get("2")

  @staticmethod
  def getRightLight(status):
    return status.get("3")

  @staticmethod
  def getSound(status, version):
    if version == 2: return status.get("0")
    else: return 0

  @staticmethod
  def getBattery(status, version):
    if version == 1: return status.get("6")
    elif version == 2: return status.get("6") % 4
    else: return 0

  @staticmethod
  def getTemperature(status, version):
    if version == 2: return status.get("6") // 4
    else: return 0

  @staticmethod
  def getAccelerometer(status, axis):
    rads = math.radians(40)
    if axis.upper() == "X":
      return status.get("13")
    elif axis.upper() == "Y":
      return math.cos(rads) * status.get("14") - math.sin(rads) * status.get("15")
    elif axis.upper() == "Z":
      return math.sin(rads) * status.get("14") + math.cos(rads) * status.get("15")
    else: return 0

  @staticmethod
  def getMagnetometer(status, axis):
    rads = math.radians(40)
    if axis.upper() == "X":
      return status.get("17")
    elif axis.upper() == "Y":
      return math.cos(rads) * status.get("18") + math.sin(rads) * status.get("19")
    elif axis.upper() == "Z":
      return math.cos(rads) * status.get("19") - math.sin(rads) * status.get("18")
    else: return 0

  @staticmethod
  def getTouch(status, version):
    if version == 2: return ((status.get("16") % 4) // 2 == 0)
    else: return False

  @staticmethod
  def getButton(status, button):
    if button.upper() == "A": return ((status.get("16") % 32) // 16 == 0)
    elif button.upper() == "B": return ((status.get("16") % 64) // 32 == 0)
    else: return False

  @staticmethod
  def getIsShaking(status):
    return (status.get("16") % 2 == 1)

  @staticmethod
  def getIsCalibrated(status):
    return ((status.get("16") % 8) // 4 == 1)
  
  @staticmethod
  def getCompass(status):
    xAccel = Status.getAccelerometer(status, "X")
    yAccel = Status.getAccelerometer(status, "Y")
    zAccel = Status.getAccelerometer(status, "Z")

    xMagnet = Status.getMagnetometer(status, "X")
    yMagnet = Status.getMagnetometer(status, "Y")
    zMagnet = Status.getMagnetometer(status, "Z")

    if zAccel != 0:
      phi = math.atan(-yAccel / zAccel)
    else:
      phi = math.pi / 2
      
    denom = yAccel * math.sin(phi) + zAccel * math.cos(phi)
    if denom != 0:
      theta = math.atan(xAccel / denom)
    else:
      theta = math.pi / 2

    xp = xMagnet
    yp = yMagnet * math.cos(phi) - zMagnet * math.sin(phi)
    zp = yMagnet * math.sin(phi) + zMagnet * math.cos(phi)
    xpp = xp * math.cos(theta) + zp * math.sin(theta)
    ypp = yp
    
    angle = 180 + math.degrees(math.atan2(xpp, ypp))
    compass = (round(angle) + 180) % 360
    return compass
  
  @staticmethod
  def combineBytes(lowByte, medByte = 0, highByte = 0):
    return highByte * 256**2 + medByte * 256 + lowByte
