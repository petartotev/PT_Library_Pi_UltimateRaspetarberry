import time
import Adafruit_DHT
from rpi_lcd import LCD
from datetime import datetime
import multiprocessing

# pinVcc = 3V3 (1)
# pinGnd = GND (9)
pinSignal = 17 # GPIO17 (11)

screen = LCD()

def getDataFromDHT11Once():
	try:
		humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pinSignal)
		return humidity, temperature
	except RuntimeError as error:
		print("Runtime error")
	except Exception as error:
		print("Exception error")

def getDataFromDHT11():
	while True:
		try:
			humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pinSignal)
			return humidity, temperature
		except RuntimeError as error:
			# Errors happen fairly often, DHT's are hard to read, just keep going.
			print("Runtime error!")
			print(error.args[0])
			continue
		except Exception as error:
			print("Exception error!")
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
		errorMessage = "Time failed!"
		screen.text(errorMessage, lineToDisplayOn)
		print(errorMessage)

def displayDataFromDHT11(isOnLine1):
	lineToDisplayOn = 1 if isOnLine1 else 2
	try:
		humidity, temperature = getDataFromDHT11Once()
		textTemp = "{:.1f}`C".format(temperature)
		textHumidity = "{}%".format(humidity)
		screen.text(textTemp + ', ' + textHumidity, lineToDisplayOn)
		print(textTemp + ', ' + textHumidity)
	except:
		errorMessage = "DHT11 failed!"
		screen.text(errorMessage, lineToDisplayOn)
		print(errorMessage)

while(True):
	#displayTime(True)
	#displayDataFromDHT11(False)
	process1 = multiprocessing.Process(target=displayTime, args=(True,))
	process2 = multiprocessing.Process(target=displayDataFromDHT11, args=(False,))
	process1.start()
	process2.start()
	time.sleep(0.9)
