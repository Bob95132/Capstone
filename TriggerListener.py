import RPi.GPIO as GPIO
import subprocess
import os
import time
import signal

#adjust for where your switch is connected
buttonPin = 11
LEDPin = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LEDPin, GPIO.OUT)

signal.signal(signal.SIGINT, GPIO.cleanup)
signal.signal(signal.SIGTERM, GPIO.cleanup)
signal.signal(signal.SIGHUP, GPIO.cleanup)

try: 
   while True:
      #assuming the script to call is long enough we can ignore bouncing
      if GPIO.input(buttonPin):
      #this is the script that will be called (as root)
         os.chdir('/home/pi/dev/Capstone')
         mount = subprocess.call('sudo mount /dev/sdb1 /mnt/usb');
         bash = subprocess.call('/home/pi/dev/Capstone/start_collection.sh')
    
         if bash == 0 and (mount == 0 or mount == 16):
            GPIO.output(LEDPin, GPIO.HIGH)
         else:
            GPIO.output(LEDPin, GPIO.LOW)
            GPIO.cleanup()
            subprocess.call('/home/pi/dev/Capstone/end_collection.sh')
      time.sleep(2)

except:
    GPIO.cleanup()
