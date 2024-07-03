# pip3 install adafruit-circuitpython-dht
# sudo apt-get install libgpiod2

import datetime
import time
import Adafruit_DHT
import os 

# pinVcc = 3V3 (1)
# pinGnd = GND (9)
pinSignal = 4 # GPIO4 (7)

def writeOutputToFile(output):
	path = 'data_temperature_dht22.txt'
	mode = 'a' if os.path.exists(path) else 'w'
	with open(path, mode) as f:
		f.write(f'{output}' + '\n')

def printOutputFriendly(humidity, temperature):
	datetime_now_str = str(datetime.datetime.now()).replace(' ', '  ')[0:20:1]
	print(f'{datetime_now_str}')
	print("Temperature: {:.2f}°C".format(temperature))
	print("   Humidity: {:.3f}%".format(humidity))
	print("~~~~~~~~~~~~~~~~~~~~~")

def printTemperatureAndHumidityForever():
	while True:
		try:
			humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pinSignal)
			#printOutputFriendly(humidity, temperature)
			output = str(datetime.datetime.now()) + " | " + "{:.2f}".format(temperature) + " | " + "{:.2f}".format(humidity)
			writeOutputToFile(output)
			print(output)
		except RuntimeError as error:
			# Errors happen fairly often, DHT's are hard to read, just keep going.
			print("Runtime error!")
			print(error.args[0])
			continue
		except Exception as error:
			print("Exception error!")
			raise error
		finally:
			time.sleep(60)

def getTemperature():
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pinSignal)
	return "{:.1f}".format(temperature)

def getHumidity():
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pinSignal)
	return "{}".format(humidity)

def getBoth():
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pinSignal)
	return "{:.2f}".format(humidity), "{:.2f}".format(temperature)

def main():
	printTemperatureAndHumidityForever()

main()
