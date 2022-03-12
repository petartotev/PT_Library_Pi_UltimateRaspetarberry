#sys.path.append("./libraries")
#import libEmailSender
import time
import datetime
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def getDistance():
	try:
		GPIO.output(TRIG, False)
		time.sleep(2)

		GPIO.output(TRIG, True)
		time.sleep(0.00001)
		GPIO.output(TRIG, False)

		while GPIO.input(ECHO) == 0:
			pulseStart = time.time()

		while GPIO.input(ECHO) == 1:
			pulseEnd = time.time()

		pulseDuration = pulseEnd - pulseStart
		distance = pulseDuration * 17150

		return distance
	except:
		gpio.cleanup()

#while(True):
#	distance = getDistance()
#	print(f'{round(distance, 2)} cm')
