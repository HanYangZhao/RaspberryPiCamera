#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time
import sys
import subprocess

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x40, debug=True)

#You'll have to calibrate this for you own servos

XservoPin = 0
YservoPin = 1
XservoRight = 180 # Min pulse length out of 4096
XservoMid = 340
XservoLeft = 512  # Max pulse length out of 4096
YservoUp = 102
YservoMid = 320
YservoDown = 440

#Tells the motion detect to stop or start
mdStop = 'echo "md 0" > /var/www/FIFO'
mdStart = 'echo "md 1" > /var/www/FIFO'
md = 0

# Not used
def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 50                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)


pwm.setPWMFreq(50)                        # Set frequency to 50 Hz or 0.2us
pwm.setPWM(XservoPin, 0, XservoMid)               # PWM 0 is the pan
pwm.setPWM(YservoPin, 0, YservoMid)               # PWM 1 is the tilt
time.sleep(1)
currentTilt = YservoMid
currentPan = XservoMid
while (True):

  pipein = open("/var/www/FIFO_piservo", 'r')
  line = pipein.readline()
  line_array = line.split(' ')
  #Reads from the FIFO_piservo file
  if line_array[0] == "servo":
    print(line_array[1])
    print(line_array[2])
    if currentTilt + int(line_array[2]) < YservoDown  and currentTilt + int(line_array[2]) > YservoUp:
      if currentPan + int(line_array[1]) < XservoLeft and currentPan + int(line_array[1]) > XservoRight:
        currentTilt += int(line_array[2])
        currentPan += int(line_array[1])
        #Stops Motion Detection
        subprocess.Popen(mdStop, shell = True)
        time.sleep(0.05)
        pwm.setPWM(YservoPin, 0, currentTilt)
        pwm.setPWM(XservoPin, 0, currentPan)

  elif line_array[0] == "led":
    p_led.createPiLight(int(line_array[1]),int(line_array[2]),int(line_array[3]))


  elif line_array[0] == "panning":
    subprocess.Popen(mdStop, shell = True)
    time.sleep(0.5)
    pwm.setPWM(XservoPin, 0, XservoLeft)               # PWM 0 is the pan
    time.sleep(1)
    currentPan = XservoLeft
    while (currentPan > 160):
      currentPan -= 1
      pwm.setPWM(XservoPin, 0, currentPan)
      time.sleep(.0225 * float(line_array[2]))
    time.sleep(1)
    pwm.setPWM(XservoPin, 0, XservoMid)
    currentPan = XservoMid 
    
  elif line_array[0] == "tilting":
    subprocess.Popen(mdStop, shell = True)
    time.sleep(0.5)
    pwm.setPWM(YservoPin, 0, YservoUp)
    time.sleep(1)
    currentTilt = YservoUp
    while (currentTilt < 440):
      currentTilt += 1
      pwm.setPWM(YservoPin, 0, currentTilt)
      time.sleep(.0225 * float(line_array[1]))
    time.sleep(1)
    pwm.setPWM(YservoPin, 0, YservoMid)
    currentTilt = YservoMid
    

  elif line_array[0] == "centering":
    print("centering")
    subprocess.Popen(mdStop, shell = True)
    time.sleep(0.25)
    pwm.setPWM(YservoPin, 0, YservoMid)               # PWM 1 is the tilt
    time.sleep(0.3)
    pwm.setPWM(XservoPin, 0, XservoMid)               # PWM 0 is the pan
    currentPan = XservoMid
    currentTilt = YservoMid
    time.sleep(1)
     

  pipein.close()
