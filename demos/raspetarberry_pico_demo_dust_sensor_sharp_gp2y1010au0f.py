"""Raspetarberry Pi project to consume DHT22 sensor data and display it on LCD screen."""

import datetime
import time

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

def print_data_from_dust_sensor():
    """Function prints data gathered from sensors."""
    p_m = ``()
    evaluation = get_air_quality_index_evaluation(p_m)
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
