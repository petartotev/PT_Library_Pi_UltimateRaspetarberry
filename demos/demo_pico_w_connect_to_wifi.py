"""Demo shows how to connect Raspberry Pico W to WiFi, then print data from 2 SPACE API-s."""

import secrets
import network
import urequests

# Create secrets.py file and save on Pico W. It should contain the following lines:
# SSID = "WIFI-SSID-HERE"
# PASSWORD = "PASSWORD-HERE"
# NASA_API_KEY = "NASA-API-KEY-HERE"

def connect_to_wifi():
    """"Connect to WiFi using network module"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    print(f'Is WIFI connected: {wlan.isconnected()}')

def get_astronauts_on_iss_from_open_notify_api():
    """"Get Names of Astronauts on ISS from OPEN NOTIFY API"""
    return urequests.get("http://api.open-notify.org/astros.json").json()

def print_astronauts_on_iss(astronauts):
    """"Print Names of Astronauts on ISS taken from OPEN NOTIFY API"""
    number = astronauts['number']
    print(f'\nCurrently, there are {number} astronauts on ISS. Their names are:')
    for i in range(number):
        print(astronauts['people'][i]['name'])

def get_apod_data_from_nasa_api():
    """Get APOD data from NASA API"""
    return urequests.get(f'https://api.nasa.gov/planetary/apod?api_key={secrets.NASA_API_KEY}').json()

def print_apod_data(data):
    """Print APOD data taken from NASA API"""
    print('\nHere is the url to the Astronomy Picture of the Day, provided by Nasa API:')
    print(f"date: {data['date']}")
    print(f"title: {data['title']}")
    print(f"explanation: {data['explanation']}")
    print(f"url: {data['url']}")

if __name__ == "__main__":
    connect_to_wifi()
    spacemen = get_astronauts_on_iss_from_open_notify_api()
    print_astronauts_on_iss(spacemen)
    result = get_apod_data_from_nasa_api()
    print_apod_data(result)
