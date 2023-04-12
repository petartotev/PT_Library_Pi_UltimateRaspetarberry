"""Raspetarberry Pi project to consume DHT22 sensor data and display it on LCD screen."""

import datetime
import time

# Sharp GP2Y1010AU0F Dust Sensor
def get_air_quality_pm():
    """Function gets particulate matter (PM) 2.5 density value from dust sensor."""
    return 0

def get_air_quality_evaluation(density):
    """Function returns a string evaluation based on PM 2.5 density."""
    if 0 <= density <= 35:
        return "excellent"
    if 35 < density <= 75:
        return "average"
    if 75 < density <= 115:
        return "light_pollution"
    if 115 < density <= 150:
        return "moderate_pollution"
    if 150 < density <= 250:
        return "heavy_pollution"
    if 250 < density <= 500:
        return "serious_pollution"
    return "unknown"

def print_data_from_dust_sensor():
    """Function prints data gathered from sensors."""
    p_m = get_air_quality_pm()
    evaluation = get_air_quality_evaluation(p_m)
    date_now = datetime.datetime.now()
    if date_now.minute == 0 or date_now.minute == 30:
        print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")},{p_m},{evaluation}')
        time.sleep(60)

def welcome():
    """Function prints welcome."""
    print("Welcome!")
    time.sleep(3)

def play():
    """Function plays the program loop."""
    welcome()
    while True:
        try:
            print_data_from_dust_sensor()
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
    """Function prints goodbye."""
    print("Bye!")
    time.sleep(3)

if __name__ == "__main__":
    try:
        play()
    except KeyboardInterrupt:
        close()
    finally:
        print("Exit!")
