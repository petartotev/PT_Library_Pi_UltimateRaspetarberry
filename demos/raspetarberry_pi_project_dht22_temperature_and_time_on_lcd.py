"""Raspetarberry Pi project to consume DHT22 sensor data and display it on LCD screen."""

import datetime
import time
import Adafruit_DHT
from rpi_lcd import LCD

screen = LCD()

# ████████████████ Line 1
# ████████████████ Line 2
# humidity: 51.53%
# temp: 21.25°C
# 2022-09-07
# 23:23:23

# pinVcc = 3V3 (1)
# pinGnd = GND (9)
PIN_SIGNAL = 4 # GPIO4 (7)

def display_text_on_lcd_screen(line1, line2, time_sleep):
    """Function displays text on LCD screen."""
    screen.text(line1, 1)
    screen.text(line2, 2)
    time.sleep(time_sleep)
    screen.clear()

def get_humidity_and_temperature():
    """Function gets data from DHT22 sensor."""
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, PIN_SIGNAL)
    return "{:.2f}%".format(humidity), "{:.2f}'C".format(temperature)

def display_humidity_and_temperature():
    """Function displays gathered data on LCD screen."""
    humidity, temperature = get_humidity_and_temperature()
    display_text_on_lcd_screen(f'humidity: {humidity}', f'temp: {temperature}', 6)

def display_date_and_time(rangerepeat):
    """Function displays date and time on LCD screen."""
    for _ in range(rangerepeat):
        datestr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").split()
        display_text_on_lcd_screen(datestr[0], datestr[1], 1)

def welcome():
    """Function displays welcome text on LCD screen."""
    screen.clear()
    screen.text('Welcome!', 1)
    time.sleep(3)

def play():
    """Function plays the program loop."""
    welcome()
    while True:
        try:
            display_humidity_and_temperature()
            time.sleep(0.5)
            display_date_and_time(6)
        except RuntimeError as error:
            # Errors occur often with DHT sensors as they are hard to read, so just keep going.
            print("Runtime error!")
            print(error.args[0])
            continue
        except Exception as error:
            print("Exception error!")
            raise error
        finally:
            time.sleep(0.5)

def close():
    """Function clears LCD screen and displays goodbye text."""
    screen.clear()
    screen.text('Goodbye...', 1)
    time.sleep(3)

def main():
    """Main function."""
    try:
        play()
    except KeyboardInterrupt:
        close()
    finally:
        screen.clear()

main()
