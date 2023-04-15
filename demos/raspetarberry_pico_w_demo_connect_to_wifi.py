import network
import secrets
import time
import urequests

# Create secrets.py file and save on Pico W. It should contain the following lines:
# SSID = "WIFI-SSID-HERE"
# PASSWORD = "PASSWORD-HERE"
# NASA_API_KEY = "NASA-API-KEY-HERE"

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    print(f'Is WIFI connected: {wlan.isconnected()}')

def get_astronauts_on_iss_from_open_notify_api():
    return urequests.get("http://api.open-notify.org/astros.json").json()

def print_astronauts_on_iss(astronauts):
    number = astronauts['number']
    print(f'\nCurrently, there are {number} astronauts on ISS. Their names are:')
    for i in range(number):
        print(astronauts['people'][i]['name'])

def get_apod_data_from_nasa_api():
    return urequests.get(f'https://api.nasa.gov/planetary/apod?api_key={secrets.NASA_API_KEY}').json()

def print_apod_data(result):
    print('\nHere is the url to the Astronomy Picture of the Day, provided by Nasa API:')
    print(f'date: {result['date']}')
    print(f'title: {result['title']}')
    print(f'explanation: {result['explanation']}')
    print(f'url: {result['url']}')

if __name__ == "__main__":
    connect_to_wifi()
    astronauts = get_astronauts_on_iss_from_open_notify_api()
    print_astronauts_on_iss(astronauts)
    result = get_apod_data_from_nasa_api()
    print_apod_data(result)