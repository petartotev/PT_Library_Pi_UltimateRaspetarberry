import datetime
import time
import Adafruit_DHT
import os 
from rpi_lcd import LCD

screen = LCD()

# ████████████████ Line 1 is 16 characters
# ████████████████ Line 2 is 16 characters
# humidity: 51.53%
# temp: 21.25°C
# 2022-09-07
# 23:23:23

# pinVcc = 3V3 (1)
# pinGnd = GND (9)
pinSignal = 4 # GPIO4 (7)

def displayTextOnLcdScreen(line1, line2, timeSleep):
	screen.text(line1, 1)
	screen.text(line2, 2)
	time.sleep(timeSleep)
	screen.clear()

def getHumidityAndTemperature():
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pinSignal)
	return "{:.2f}%".format(humidity), "{:.2f}'C".format(temperature)

def displayHumidityAndTemperature():
    humidity, temperature = getHumidityAndTemperature()
    displayTextOnLcdScreen(f'humidity: {humidity}', f'temp: {temperature}', 6)

def displayDateAndTime(rangerepeat):
    for x in range(rangerepeat):
        datestr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").split()
        displayTextOnLcdScreen(datestr[0], datestr[1], 1)

def welcome():
    screen.clear()
    screen.text('Welcome!', 1)
    time.sleep(3)

def play():
    welcome()
    while True:
        try:
            displayHumidityAndTemperature()
            time.sleep(0.5)
            displayDateAndTime(6)
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going.
            print("Runtime error!")
            print(error.args[0])
            continue
        except Exception as error:
            print("Exception error!")
            raise error
        finally:
            time.sleep(0.5)

def close():
    screen.clear()
    screen.text('Goodbye...', 1)
    time.sleep(3)

def main():
    try:
        play()
    except KeyboardInterrupt:
        close()
    finally:
        screen.clear()

main()
