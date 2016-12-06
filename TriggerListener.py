import RPi.GPIO as GPIO
import subprocess
import os
import time

#adjust for where your switch is connected
buttonPin = 17
LEDPin = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LEDPin, GPIO.OUT)

while True:
  #assuming the script to call is long enough we can ignore bouncing
  if GPIO.input(buttonPin):
    #this is the script that will be called (as root)
    os.chdir('/home/pi/dev/Capstone')
    bash = subprocess.call('/home/pi/dev/Capstone/start_collection.sh')
    if bash == 0:
      GPIO.output(LEDPin, GPIO.HIGH)
    else:
       GPIO.output(LEDPin, GPIO.LOW)
       subprocess.call('/home/pi/dev/Capstone/end_collection.sh')
    time.sleep(2)
