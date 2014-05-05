#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x40, debug=True)


XservoPin = 0
YservoPin = 1 
XservoRight = 180 # Min pulse length out of 4096
XservoMid = 340
XservoLeft = 512  # Max pulse length out of 4096
YservoUp = 102
YservoMid = 320
YservoDown = 440

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 50                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(50)                        # Set frequency to 50 Hz
pwm.setPWM(XservoPin, 0, XservoMid)               # PWM 0 is the pan
pwm.setPWM(YservoPin, 0, YservoMid)               # PWM 1 is the tilt
time.sleep(1)
currentTilt = YservoMid 
currentPan = XservoMid
#log = open("/home/pi/bin/servo/log", 'w')
while (True):

  pipein = open("/var/www/FIFO_piservo", 'r')
 # log.write("opened")
 # log.write("\n")
  line = pipein.readline()
  line_array = line.split(' ')
  if line_array[0] == "servo":
    if currentTilt + int(line_array[2]) < YservoDown  and currentTilt + int(line_array[2]) > YservoUp:
      if currentPan + int(line_array[1]) < XservoLeft and currentPan + int(line_array[1]) > XservoRight:
        prevTilt = currentTilt
        prevPan = currentPan
        currentTilt += int(line_array[2])
        currentPan += int(line_array[1])
        for y in range(0, abs(currentTilt - prevTilt)):
          if(currentTilt - prevTilt < 0):
            pwm.setPWM(YservoPin, 0, currentTilt -  y)
          else:    
            pwm.setPWM(YservoPin, 0, currentTilt + y)
          time.sleep(0.015)
        for x in range(0, abs(currentPan - prevPan)):
          if(currentPan - prevPan < 0):
            pwm.setPWM(XservoPin, 0, currentPan - x)
          else:
            pwm.setPWM(XservoPin, 0, currentPan + x)
          time.sleep(0.015)
         
  elif line_array[0] == "led":
    p_led.createPiLight(int(line_array[1]),int(line_array[2]),int(line_array[3]))
 

  elif line_array[0] == "panning":
    print("panning")
    pwm.setPWM(XservoPin, 0, XservoLeft)               # PWM 0 is the pan
    time.sleep(1)
    currentPan = XservoLeft
    while (currentPan > 160):
      currentPan -= 1 
      pwm.setPWM(XservoPin, 0, currentPan)
      time.sleep(.0225)
    time.sleep(1)
    pwm.setPWM(XservoPin, 0, XservoMid)
    currentPan = XservoMid

  elif line_array[0] == "centering":
    pwm.setPWM(YservoPin, 0, YservoMid)               # PWM 1 is the tilt
    time.sleep(0.3)
    pwm.setPWM(XservoPin, 0, XservoMid)               # PWM 0 is the pan
    currentPan = XservoMid
    currentTilt = YservoMid
    time.sleep(1)
  pipein.close()
