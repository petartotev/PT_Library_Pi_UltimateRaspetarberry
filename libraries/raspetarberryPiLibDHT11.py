# pip3 install adafruit-circuitpython-dht
# sudo apt-get install libgpiod2

import time
import Adafruit_DHT

# pinVcc = 3V3 (1)
# pinGnd = GND (9)
pinSignal = 17 # GPIO17 (11)

def printTemperatureAndHumidityForever():
	while True:
		try:
			humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pinSignal)
			print("Temperature: {:.1f}°C.".format(temperature))
			print("Humidity: {}%.".format(humidity))
		except RuntimeError as error:
			# Errors happen fairly often, DHT's are hard to read, just keep going.
			print("Runtime error!")
			print(error.args[0])
			continue
		except Exception as error:
			print("Exception error!")
			raise error
		finally:
			time.sleep(3)

def getTemperature():
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pinSignal)
	return "{:.1f}".format(temperature)

def getHumidity():
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pinSignal)
	return "{}".format(humidity)

def getBoth():
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pinSignal)
	return "{}".format(humidity), "{:.1f}".format(temperature)
