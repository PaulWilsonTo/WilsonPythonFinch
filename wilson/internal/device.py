'''
  © Paul Wilson 2021
    Published under the Simple Public License:
    https://opensource.org/licenses/Simple-2.0
  For controlling BirdBrain Technologies Finch 2.0
    with Java and Python in online IDE like ReplIt
    see https://www.birdbraintechnologies.com/
'''
import math
from wilson.internal.common import debug

class Device():
  @staticmethod
  def getCalibrationBytes():
    return [0xCE, 0xFF, 0xFF, 0xFF]
    
  @staticmethod
  def getResetTicksBytes():
    return [0xD5]

  @staticmethod
  def getStopAllBytes():
    return [0xDF]
  
  @staticmethod
  def getRunMotorsBytes(leftSpeedFactor, rightSpeedFactor):
    leftMotorSpeed = Device.getMotorSpeed(abs(leftSpeedFactor), leftSpeedFactor > 0)
    rightMotorSpeed = Device.getMotorSpeed(abs(rightSpeedFactor), rightSpeedFactor > 0)
    return [0xD2, 0x40,
      leftMotorSpeed, 0, 0, 0,
      rightMotorSpeed, 0, 0, 0
    ]
  
  @staticmethod
  def getForwardBytes(distance, speedFactor):
    motorSpeed = Device.getMotorSpeed(speedFactor, distance >= 0)
    moveTicks = Device.getMoveTicks(distance)
    tickBytes = Device.splitBytes(moveTicks)
    return [0xD2, 0x40,
      motorSpeed, tickBytes[2], tickBytes[1], tickBytes[0],
      motorSpeed, tickBytes[2], tickBytes[1], tickBytes[0]
    ]
      
  @staticmethod
  def getRightBytes(angle, speedFactor):
    leftSpeed = Device.getMotorSpeed(speedFactor, angle > 0)
    rightSpeed = Device.getMotorSpeed(speedFactor, angle < 0)
    turnTicks = Device.getTurnTicks(angle)
    tickBytes = Device.splitBytes(turnTicks)
    return [0xD2, 0x40,
      leftSpeed , tickBytes[2], tickBytes[1], tickBytes[0],
      rightSpeed, tickBytes[2], tickBytes[1], tickBytes[0]
    ]
  
  @staticmethod
  def getLightBytes(beak, tail1, tail2, tail3, tail4):
    return [0xD0, beak[0], beak[1], beak[2],
      tail1[0], tail1[1], tail1[2],
      tail2[0], tail2[1], tail2[2],
      tail3[0], tail3[1], tail3[2],
      tail4[0], tail4[1], tail4[2],
      0x00, 0x00, 0x00, 0x00
    ]

  @staticmethod
  def getLedFlashBytes(phrase):
    listBytes = []
    for letter in phrase:
      listBytes.append([0xD2, 0x01, ord(letter)]) #([0xCC, 0x41, ord(letter)])
    return listBytes
  
  @staticmethod
  def getLedGridBytes(ledGrid):
    try:
      leds = ledGrid.getList()
      led25only = (leds[24] if 1 else 0)
      led24to17 = 0
      for index in range(16, 24):
        led24to17 += (leds[index] if 1 else 0) * 2**(index - 16)
      led16to09 = 0
      for index in range(8, 16):
        led16to09 += (leds[index] if 1 else 0) * 2**(index - 8)
      led08to01 = 0
      for index in range(0, 8):
        led08to01 += (leds[index] if 1 else 0) * 2**(index)
      return [0xD2, 0x20, led25only, led24to17, led16to09, led08to01] #[0xCC, 0x80, led25only, led24to17, led16to09, led08to01]
    except:
      return [0xD2, 0x20, 0, 0, 0, 0] #[0xCC, 0x00, 0xFF, 0xFF, 0xFF]
  
  @staticmethod
  def getMusicBytes(music):
    listBytes = []
    for sound in music.getList():
      midiNote = sound.get("midiNote")
      duration = sound.get("duration")
      
      if midiNote > 0:
        frequency = 440 * 2**((midiNote - 69) / 12)
        period = round(1000000 / frequency)
      else:
        period = 0
        
      noteBytes = Device.splitBytes(period)
      timeBytes = Device.splitBytes(duration)

      #listBytes.append([0x90, noteBytes[1], noteBytes[0],
      #  timeBytes[1], 0x20, timeBytes[0], 0x00, 0x00
      #])
      listBytes.append([0xD0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, # TODO Lights
        noteBytes[1], noteBytes[0], timeBytes[1], timeBytes[0]
      ])
    return listBytes

  @staticmethod
  def getMotorSpeed(speedFactor, isForward):
    motorSpeed = round(36 * speedFactor / 10)
    if motorSpeed < 3: motorSpeed = 0
    if motorSpeed > 0 and isForward: motorSpeed += 128
    return motorSpeed
  
  @staticmethod
  def getMoveTicks(distance):
    return math.floor(49.7 * abs(distance))
  
  @staticmethod
  def getTurnTicks(angle):
    return math.floor(4.335 * abs(angle))

  @staticmethod
  def splitBytes(number):
    lowByte = number % 256
    medByte = (number // 256) % 256
    highByte = (number // 256**2) % 256
    return [lowByte, medByte, highByte]
