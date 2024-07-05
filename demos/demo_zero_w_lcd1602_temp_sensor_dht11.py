"""Python script implements DHT11 Temperature Sensor using LCD 1602 Screen"""

import time
import multiprocessing
import Adafruit_DHT
from rpi_lcd import LCD
from datetime import datetime

screen = LCD()

# pinVcc = 3V3 (1)
# pinGnd = GND (9)
PIN_SIGNAL = 17 # GPIO17 (11)

ERROR_MESSAGE_GET_DATA_DHT11_RUNTIME = "ERROR: Runtime error while executing get_dht11_data!"
ERROR_MESSAGE_GET_DATA_DHT11 = "ERROR: Exception while executing get_dht11_data!"
ERROR_MESSAGE_DISPLAY_TIME = "ERROR: datetime.now() or parsing it failed on displayTime(WithLock)!"
ERROR_MESSAGE_DISPLAY_DATA_DHT11 = "ERROR: Either get_dht11_data_once() or parsing it failed on display_dht11_data(WithLock)!"

ERR_DISPLAY_TIME = "ERR:displayTime"
ERR_DISPLAY_DHT11 = "ERR:displayDHT11"

lock = multiprocessing.Lock()

def run_demo():
    """Run demo"""
    try:
        while True:
            #displayTime(True)
            #display_dht11_data(False)
            process1 = multiprocessing.Process(target=display_time_with_lock, args=(True, lock))
            process2 = multiprocessing.Process(target=display_dht11_data_with_lock, args=(False, lock))
            process1.start()
            process2.start()
            time.sleep(0.95)
    except KeyboardInterrupt:
        screen.clear()

def get_dht11_data_once():
    """Get data from DHT11 only once"""
    try:
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, PIN_SIGNAL)
        return humidity, temperature
    except RuntimeError as error:
        print(ERROR_MESSAGE_GET_DATA_DHT11_RUNTIME + f' {str(error)}')
    except Exception as error:
        print(ERROR_MESSAGE_GET_DATA_DHT11 + f' {str(error)}')

def get_dht11_data():
    """Get data from DHT11"""
    while True:
        try:
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, PIN_SIGNAL)
            return humidity, temperature
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going.
            print(ERROR_MESSAGE_GET_DATA_DHT11_RUNTIME)
            print(error.args[0])
            continue
        except Exception as error:
            print(ERROR_MESSAGE_GET_DATA_DHT11)
            raise error
        finally:
            time.sleep(5)

def display_time(is_on_line_1):
    """Display Time"""
    line_to_display_on = 1 if is_on_line_1 else 2
    try:
        datetimenow = str(datetime.now()).replace('-','')
        text_date = datetimenow[2:8]
        text_time = datetimenow[9:17]
        screen.text(text_time + '  ' + text_date, line_to_display_on)
        print(text_time + '  ' + text_date)
    except Exception:
        screen.text(ERR_DISPLAY_TIME, line_to_display_on)
        print(ERR_DISPLAY_TIME)

def display_time_with_lock(is_on_line_1, lock_it):
    """Display Time with Lock"""
    line_to_display_on = 1 if is_on_line_1 else 2
    try:
        datetimenow = str(datetime.now()).replace('-','')
        text_date = datetimenow[2:8]
        text_time = datetimenow[9:17]
        with lock_it:
            try:
                screen.text(text_time + '  ' + text_date, line_to_display_on)
                print(text_time + '  ' + text_date)
            except Exception:
                screen.text(ERR_DISPLAY_TIME, line_to_display_on)
                print(ERR_DISPLAY_TIME)
    except Exception:
        print(ERROR_MESSAGE_DISPLAY_TIME)

def display_dht11_data(is_on_line_1):
    """Display DHT11 Data"""
    line_to_display_on = 1 if is_on_line_1 else 2
    try:
        humidity, temperature = get_dht11_data_once()
        text_temp = "{:.1f}`C".format(temperature)
        text_humidity = "{}%".format(humidity)
        screen.text(text_temp + ', ' + text_humidity, line_to_display_on)
        print(text_temp + ', ' + text_humidity)
    except Exception:
        screen.text(ERR_DISPLAY_DHT11, line_to_display_on)
        print(ERR_DISPLAY_DHT11)

def display_dht11_data_with_lock(is_on_line_1, lock_it):
    """Display DHT11 Data with Lock"""
    line_to_display_on = 1 if is_on_line_1 else 2
    try:
        humidity, temperature = get_dht11_data_once()
        text_temp = "{:.1f}`C".format(temperature)
        text_humidity = "{}%".format(humidity)
        with lock_it:
            try:
                screen.text(text_temp + ', ' + text_humidity, line_to_display_on)
                print(text_temp + ', ' + text_humidity)
            except Exception:
                screen.text(ERR_DISPLAY_DHT11, line_to_display_on)
                print(ERR_DISPLAY_DHT11)
    except Exception:
        print(ERROR_MESSAGE_DISPLAY_DATA_DHT11)

run_demo()
