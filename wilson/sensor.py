'''
  © Paul Wilson 2021
    Published under the Simple Public License:
    https://opensource.org/licenses/Simple-2.0
  For controlling BirdBrain Technologies Finch 2.0
    with Java and Python in online IDE like ReplIt
    see https://www.birdbraintechnologies.com/
'''
from wilson.internal.status import Status

class Sensor():
  def __init__(self, status, version):
    self.__status = status
    self.__version = version

  def isWorking(self):
    return Status.getIsWorking(self.__status)
  
  def wallDistance(self):
    return 0.091 * Status.getDistance(self.__status, self.__version)
  
  def leftDistance(self):
    return Status.getLeftTicks(self.__status) / 49.700
  
  def rightDistance(self):
    return Status.getRightTicks(self.__status) / 49.700
  
  def leftLine(self):
    return Status.getLeftLine(self.__status)
  
  def rightLine(self):
    return Status.getRightLine(self.__status)
  
  def leftLight(self):
    return Status.getLeftLight(self.__status)
  
  def rightLight(self):
    return Status.getRightLight(self.__status)
  
  def sound(self):
    return Status.getSound(self.__status, self.__version)
  
  def battery(self):
    return Status.getBattery(self.__status, self.__version)
  
  def temperature(self):
    return Status.getTemperature(self.__status, self.__version)
  
  def accelerometer(self, axis):
    return Status.getAccelerometer(self.__status, axis)
  
  def magnetometer(self, axis):
    return Status.getMagnetometer(self.__status, axis)
  
  def touch(self):
    return Status.getTouch(self.__status, self.__version)
  
  def button(self, button):
    return Status.getButton(self.__status, button)
  
  def isShaking(self):
    return Status.getIsShaking(self.__status)
  
  def calibrated(self):
    return Status.getIsCalibrated(self.__status)
  
  def compass(self):
    return Status.getCompass(self.__status)

  def rawData(self):
    data = []
    for index in range(20):
      data.append(self.__status.get(str(index)))
    return data
