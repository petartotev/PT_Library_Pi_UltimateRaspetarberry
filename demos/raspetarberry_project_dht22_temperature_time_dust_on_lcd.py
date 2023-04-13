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
# PM2.5: 500 μg/m3
# Excellent
# Average
# Light poll
# Moderate poll!
# Heavy poll!!
# Serious poll!!!
# pinVcc = 3V3 (1)
# pinGnd = GND (9)

PIN_SIGNAL = 4 # GPIO4 (7)

# DHT22 AM2302 Temperature and Humidity Sensor
def get_humidity_and_temperature():
    """Function gets data from DHT22 sensor."""
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, PIN_SIGNAL)
    return "{:.2f}%".format(humidity), "{:.2f}'C".format(temperature)

# Sharp GP2Y1010AU0F Dust Sensor
def get_air_quality_particulate_matter():
    """Function gets particulate matter PM2.5 density value from dust sensor."""
    return 0

def get_air_quality_index_evaluation(density):
    """Function returns EPA AQI evaluation based on PM2.5 density."""
    if 0 <= density < 12:
        return "Good"
    if 12 <= density < 35:
        return "Moderate"
    if 35 <= density < 55:
        return "Unhealthy for Sensitive Groups"
    if 55 <= density < 150:
        return "Unhealthy"
    if 150 <= density < 250:
        return "Very Unhealthy"
    if 250 <= density <= 500:
        return "Hazardous"
    return "Unknown"

# LCD 1602
def display_text_on_lcd_screen(line1, line2, time_sleep):
    """Function displays text on LCD screen."""
    screen.text(line1, 1)
    screen.text(line2, 2)
    time.sleep(time_sleep)
    screen.clear()

def display_date_and_time(rangerepeat):
    """Function displays date and time on LCD screen."""
    for _ in range(rangerepeat):
        datestr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").split()
        display_text_on_lcd_screen(datestr[0], datestr[1], 1)

def display_data_from_sensors():
    """Function displays data gathered from sensors on LCD screen."""
    humidity, temperature = get_humidity_and_temperature()
    p_m = get_air_quality_particulate_matter()
    evaluation = get_air_quality_index_evaluation(p_m)
    date_now = datetime.datetime.now()
    if date_now.minute == 0 or date_now.minute == 30:
        with open("/home/pi/Desktop/repos/PT_Library_Pi_UltimateRaspetarberry/temp.csv", "a") as mytemp:
            mytemp.write(f'{date_now},{temperature},{humidity}\n')
        with open("/home/pi/Desktop/repos/PT_Library_Pi_UltimateRaspetarberry/dust.csv", "a") as mydust:
            mydust.write(f'{date_now},{p_m}ug/m3\n')
        time.sleep(60)
    display_text_on_lcd_screen(f'humidity: {humidity}', f'temp: {temperature}', 6)
    display_text_on_lcd_screen(f'PM2.5: {p_m} ug/m3', evaluation, 4)

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
            display_data_from_sensors()
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

if __name__ == "__main__":
    try:
        play()
    except KeyboardInterrupt:
        close()
    finally:
        screen.clear()
