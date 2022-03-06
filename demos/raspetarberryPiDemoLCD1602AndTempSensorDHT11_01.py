import time
import multiprocessing
import Adafruit_DHT
from rpi_lcd import LCD
from datetime import datetime

screen = LCD()

# pinVcc = 3V3 (1)
# pinGnd = GND (9)
pinSignal = 17 # GPIO17 (11)

errorMessageGetDataDHT11Runtime = "ERROR: Runtime error while executing getDataFromDHT11!"
errorMessageGetDataDHT11 = "ERROR: Exception while executing getDataFromDHT11!"
errorMessageDisplayTime = "ERROR: Either datetime.now() or parsing its result failed while executing displayTime(WithLock)!"
errorMessageDisplayDataDHT11 = "ERROR: Either getDataFromDHT11Once() or parsing its result failed while executing displayDataFromDHT11(WithLock)!"

errDisplayTime = "ERR:displayTime"
errDisplayDHT11 = "ERR:displayDHT11"

lock = multiprocessing.Lock()

def runDemo():
	while(True):
		#displayTime(True)
		#displayDataFromDHT11(False)
		process1 = multiprocessing.Process(target=displayTimeWithLock, args=(True, lock))
		process2 = multiprocessing.Process(target=displayDataFromDHT11WithLock, args=(False, lock))
		process1.start()
		process2.start()
		time.sleep(0.95)

def getDataFromDHT11Once():
	try:
		humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pinSignal)
		return humidity, temperature
	except RuntimeError as error:
		print(errorMessageGetDataDHT11Runtime)
	except Exception as error:
		print(errorMessageGetDataDHT11)

def getDataFromDHT11():
	while True:
		try:
			humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pinSignal)
			return humidity, temperature
		except RuntimeError as error:
			# Errors happen fairly often, DHT's are hard to read, just keep going.
			print(errorMessageGetDataDHT11Runtime)
			print(error.args[0])
			continue
		except Exception as error:
			print(errorMessageGetDataDHT11)
			raise error
		finally:
			time.sleep(5)

def displayTime(isOnLine1):
	lineToDisplayOn = 1 if isOnLine1 else 2
	try:
		datetimenow = str(datetime.now()).replace('-','')
		textDate = datetimenow[2:8]
		textTime = datetimenow[9:17]
		screen.text(textTime + '  ' + textDate, lineToDisplayOn)
		print(textTime + '  ' + textDate)
	except:
		screen.text(errDisplayTime, lineToDisplayOn)
		print(errDisplayTime)

def displayTimeWithLock(isOnLine1, lock):
	lineToDisplayOn = 1 if isOnLine1 else 2
	try:
		datetimenow = str(datetime.now()).replace('-','')
		textDate = datetimenow[2:8]
		textTime = datetimenow[9:17]
		with lock:
			try:
				screen.text(textTime + '  ' + textDate, lineToDisplayOn)
				print(textTime + '  ' + textDate)
			except:
				screen.text(errDisplayTime, lineToDisplayOn)
				print(errDisplayTime)
	except:
		print(errorMessageDisplayTime)

def displayDataFromDHT11(isOnLine1):
	lineToDisplayOn = 1 if isOnLine1 else 2
	try:
		humidity, temperature = getDataFromDHT11Once()
		textTemp = "{:.1f}`C".format(temperature)
		textHumidity = "{}%".format(humidity)
		screen.text(textTemp + ', ' + textHumidity, lineToDisplayOn)
		print(textTemp + ', ' + textHumidity)
	except:
		screen.text(errDisplayDHT11, lineToDisplayOn)
		print(errDisplayDHT11)

def displayDataFromDHT11WithLock(isOnLine1, lock):
	lineToDisplayOn = 1 if isOnLine1 else 2
	try:
		humidity, temperature = getDataFromDHT11Once()
		textTemp = "{:.1f}`C".format(temperature)
		textHumidity = "{}%".format(humidity)
		with lock:
			try:
				screen.text(textTemp + ', ' + textHumidity, lineToDisplayOn)
				print(textTemp + ', ' + textHumidity)
			except:
				screen.text(errDisplayDHT11, lineToDisplayOn)
				print(errDisplayDHT11)
	except:
		print(errorMessageDisplayDataDHT11)

runDemo()
