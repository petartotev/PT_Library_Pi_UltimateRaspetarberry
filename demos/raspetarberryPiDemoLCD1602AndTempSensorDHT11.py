import time
import Adafruit_DHT
from rpi_lcd import LCD
from datetime import datetime
import threading

# pinVcc = 3V3 (1)
# pinGnd = GND (9)
pinSignal = 17 # GPIO17 (11)

screen = LCD()

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
	datetimenow = str(datetime.now()).replace('-','')
	textDate = datetimenow[2:8]
	textTime = datetimenow[9:17]
	screen.text(textTime + '  ' + textDate, lineToDisplayOn)

def displayDataFromDHT11(isOnLine1):
	lineToDisplayOn = 1 if isOnLine1 else 2
	humidity, temperature = getDataFromDHT11()
	textTemp = "{:.1f}`C".format(temperature)
	textHumidity = "{}%".format(humidity)
	screen.text(textTemp + ', ' + textHumidity, lineToDisplayOn)

while(True):
	displayTime(True)
	displayDataFromDHT11(False)
	#th = threading.Thread(target=displayDataFromDHT11(False))
	#th.start()
