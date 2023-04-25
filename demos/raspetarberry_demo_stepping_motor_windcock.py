'''Windcock'''

import time
import http.client
import json
import datetime
import sys
import credentials
import geocoder
import requests
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# STEPPING MOTOR

WAIT_TIME = 0.001

StepPins = [24,25,8,7]

for pin in StepPins:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, False)

STEP_COUNT_1 = 4
Seq1 = []
Seq1 = [i for i in range(0, STEP_COUNT_1)]
Seq1[0] = [1,0,0,0]
Seq1[1] = [0,1,0,0]
Seq1[2] = [0,0,1,0]
Seq1[3] = [0,0,0,1]

STEP_COUNT_2 = 8
Seq2 = []
Seq2 = [i for i in range(0, STEP_COUNT_2)]
Seq2[0] = [1,0,0,0]
Seq2[1] = [1,1,0,0]
Seq2[2] = [0,1,0,0]
Seq2[3] = [0,1,1,0]
Seq2[4] = [0,0,1,0]
Seq2[5] = [0,0,1,1]
Seq2[6] = [0,0,0,1]
Seq2[7] = [1,0,0,1]

Seq = Seq2
STEP_COUNT = STEP_COUNT_2

def steps(n_b):
    '''Steps'''
    step_counter = 0
    sign = -1 if n_b < 0 else 1
    n_b = sign * n_b * 2 # times 2 because half-step
    print(f'n_bsteps {n_b} and sign {sign}')
    for _ in range(n_b):
        for pin in range(4):
            xpin = StepPins[pin]
            GPIO.output(xpin, True if Seq[step_counter][pin]!=0 else False)
        step_counter += sign
    # If we reach the end of the sequence => start again
        if step_counter == STEP_COUNT:
            step_counter = 0
        if step_counter < 0:
            step_counter = STEP_COUNT - 1
        time.sleep(WAIT_TIME)

# OPEN WEATHER API

URL_API_IPIFY_ORG = 'https://api.ipify.org'
URL_OPEN_WEATHER_API = 'api.openweathermap.org'
OPEN_WEATHER_API_KEY = credentials.getWeatherApiKey()

def get_offset_from_utc_to_local():
    '''Get offset from UTC to Local'''
    now = time.time()
    offset = datetime.datetime.fromtimestamp(now) - datetime.datetime.utcfromtimestamp(now)
    return int(offset.seconds / 3600)

def get_weather_api_response(lat, lon, key_weather_api):
    '''Get Weather API response'''
    url_weather_api = f'/data/2.5/weather?lat={lat}&lon={lon}&appid={key_weather_api}'
    conn = http.client.HTTPSConnection(URL_OPEN_WEATHER_API)
    conn.request("GET", url_weather_api)
    response = conn.getresponse()
    return json.loads(response.read().decode("utf-8"))

def extract_wind_from_weather_api_response(response):
    '''Extract wind from Weather API response'''
    return response["wind"]["deg"], response["wind"]["speed"]

def extract_time_from_weather_api_response(response):
    '''Extract time from Weather API response'''
    return response["dt"]

def convert_degree_to_unit(degree):
    '''Convert degree to unit'''
    return round((2048 * round(degree)) / 360)

def convert_unit_to_degree(unit):
    '''Convert unit to degree'''
    return round((360 * round(unit)) / 2048)

def get_lat_and_long_by_ip_address():
    '''Get latitude and longitude based on current public ip address'''
    ip_public = requests.get(URL_API_IPIFY_ORG, timeout=10).text
    geo = geocoder.ip(ip_public)
    return geo.latlng[0], geo.latlng[1]

def get_coordinates_from_run_args_or_ip():
    '''Get coordinates from run arguments or from current public ip address'''
    city = str(sys.argv[1]) if len(sys.argv) > 1 else "Undefined"
    if city == "CherniVruh":
        return 42.56378836361624, 23.278416348642256
    if city == "Sofia":
        return 42.68232568553703, 23.335369831287874
    if city == "Burgas":
        return 42.493969995866784, 27.46136420793039
    response = get_lat_and_long_by_ip_address()
    return response[0], response[1]

def get_direction_abbr_by_degree(degree):
    '''Get direction abbreviation from degree'''
    if degree >= 348.75 or degree < 11.25:
        return "N"
    if 11.25 <= degree < 33.75:
        return "NNE"
    if 33.75 <= degree < 56.25:
        return "NE"
    if 56.25 <= degree < 78.75:
        return "ENE"
    if 78.75 <= degree < 101.25:
        return "E"
    if 101.25 <= degree < 123.75:
        return "ESE"
    if 123.75 <= degree < 146.25:
        return "SE"
    if 146.25 <= degree < 168.75:
        return "SSE"
    if 168.75 <= degree < 191.25:
        return "S"
    if 191.25 <= degree < 213.75:
        return "SSW"
    if 213.75 <= degree < 236.25:
        return "SW"
    if 236.25 <= degree < 258.75:
        return "WSW"
    if 258.75 <= degree < 281.25:
        return "W"
    if 281.25 <= degree < 303.75:
        return "WNW"
    if 303.75 <= degree < 326.25:
        return "NW"
    if 326.25 <= degree < 348.75:
        return "NNW"
    return "Unknown"

# PROGRAM

def main():
    '''Main program'''
    coords = get_coordinates_from_run_args_or_ip()
    print(f'Latitude is {coords[0]}, Longitude is {coords[1]}.\n')
    dir_curr_unit = 0
    try:
        while True:
            #print(f'dir_curr_unit before update: {dir_curr_unit}')
            try:
                data = get_weather_api_response(coords[0], coords[1], OPEN_WEATHER_API_KEY)
            except KeyboardInterrupt:
                steps(dir_curr_unit if dir_curr_unit < 1024 else -(2048 - dir_curr_unit))
                sys.exit("Keyboard interrupt! Exit!")
            except:
                steps(dir_curr_unit if dir_curr_unit < 1024 else -(2048 - dir_curr_unit))
                dir_curr_unit = 0
                print("ERROR: Request to Weather API failed!")
                time.sleep(10)
                continue
            time_taken = datetime.datetime.utcfromtimestamp(int(data["dt"]))
            hour_taken = time_taken.hour + get_offset_from_utc_to_local()
            minute_taken = time_taken.minute
            print(f'Wind data taken at {hour_taken:0>2}:{minute_taken:0>2}')
            wind_data = extract_wind_from_weather_api_response(data)
            print(f'New Speed: {wind_data[1]} mps')
            dir_data_degree = round(wind_data[0])
            dir_new_unit = convert_degree_to_unit(dir_data_degree)
            print(f'New Direction: {dir_data_degree}° ({dir_new_unit} units)')
            if dir_new_unit >= dir_curr_unit:
                diff = dir_new_unit - dir_curr_unit
                steps(-diff)
                dir_curr_unit = dir_curr_unit + diff
            else:
                diff = dir_curr_unit - dir_new_unit
                steps(diff)
                dir_curr_unit = dir_curr_unit - diff
            dir_curr_degree = convert_unit_to_degree(dir_curr_unit)
            abbr = get_direction_abbr_by_degree(dir_curr_degree)
            print(f'Current Direction: {dir_curr_degree}° ({dir_curr_unit} units), {abbr}\n')
            date = datetime.datetime.now()
            if date.minute in (0,30):
                with open("wind.csv", "a", encoding="utf-8") as mywind:
                    mywind.write(f'{date},{dir_curr_degree}°,{dir_curr_unit} units,{abbr}\n')
            time.sleep(60)
    except KeyboardInterrupt:
        if dir_curr_unit < 1024:
            steps(dir_curr_unit)
        else:
            steps(-(2048 - dir_curr_unit))

if __name__ == '__main__':
    main()
