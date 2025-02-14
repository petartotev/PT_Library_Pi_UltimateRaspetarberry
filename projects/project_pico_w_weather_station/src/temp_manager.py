"""
temp_manager - DHT22 Temperature and Humidity Sensor
"""

import dht
from machine import Pin


dht_sensor = dht.DHT22(Pin(16)) # Initialize DHT22 sensor on GP16


def get_data_from_dht22_sensor():
    """
    Reads temperature and humidity from the DHT22 sensor.

    Returns:
        tuple: (temperature, humidity) in Celsius and percentage.
               Returns (None, None) on failure.
    """
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()  # °C
        humidity = dht_sensor.humidity()        # %
        return temperature, humidity

    except OSError as e:
        print(f"OSError! Failed to read DHT22 sensor: {e}")
        return None, None