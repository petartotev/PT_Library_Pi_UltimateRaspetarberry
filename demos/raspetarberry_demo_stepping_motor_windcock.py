'''Windock'''

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
    if n_b < 0:
        sign = -1
    else:
        sign = 1
    n_b = sign * n_b * 2 # times 2 because half-step
    print(f'n_bsteps {n_b} and sign {sign}')
    for _ in range(n_b):
        for pin in range(4):
            xpin = StepPins[pin]
            if Seq[step_counter][pin]!=0:
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)
        step_counter += sign
    # If we reach the end of the sequence => start again
        if step_counter == STEP_COUNT:
            step_counter = 0
        if step_counter < 0:
            step_counter = STEP_COUNT - 1
        # Wait before moving on
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
    data = response.read()
    data_decoded = data.decode("utf-8")
    return json.loads(data_decoded)

def extract_wind_from_weather_api_response(response):
    '''Extract wind from Weather API response'''
    wind_direction = response["wind"]["deg"]
    wind_speed = response["wind"]["speed"]
    return wind_direction, wind_speed

def extract_time_from_weather_api_response(response):
    '''Extract time from Weather API response'''
    return response["dt"]

def convert_degree_to_unit(degree):
    '''Convert degree to unit'''
    return round((2048 * round(degree)) / 360)

def convert_unit_to_degree(unit):
    '''Convert unit to degree'''
    return round((360 * round(unit)) / 2048)

def get_lat_and_lon_by_ip_address():
    '''Get latitude and longitude based on current public ip address'''
    ip_public = requests.get(URL_API_IPIFY_ORG, timeout=10).text
    geo = geocoder.ip(ip_public)
    lat = geo.latlng[0]
    lon = geo.latlng[1]
    return lat, lon

def get_coordinates_from_run_args_or_ip():
    '''Get coordinates from run arguments or current public ip address'''
    if len(sys.argv) > 1:
        city = str(sys.argv[1])
    else:
        city = "Undefined"
    if city == "CherniVruh":
        lat = 42.56378836361624
        lon =  23.278416348642256
    elif city == "Sofia":
        lat = 42.68232568553703
        lon = 23.335369831287874
    elif city == "Burgas":
        lat = 42.493969995866784
        lon = 27.46136420793039
    else:
        response = get_lat_and_lon_by_ip_address()
        lat = response[0]
        lon = response[1]
    return lat, lon

# PROGRAM

def main():
    '''Main program'''
    coords = get_coordinates_from_run_args_or_ip()
    lat = coords[0]
    lon = coords[1]
    deg_curr = 0
    print(f'Lat is {lat}, Lon is {lon}.')
    print('~')
    try:
        while True:
            #print(f'deg_curr before update: {deg_curr}')
            try:
                data = get_weather_api_response(lat, lon, OPEN_WEATHER_API_KEY)
            except KeyboardInterrupt:
                if deg_curr < 1024:
                    steps(deg_curr)
                else:
                    steps(-(2048 - deg_curr))
                sys.exit("Keyboard interrupt! Exit!")
            except:
                if (deg_curr < 1024):
                    steps(deg_curr)
                else:
                    steps(-(2048 - deg_curr))
                deg_curr = 0
                print("ERROR: Request to Weather API failed!")
                time.sleep(10)
                continue
            time_taken = datetime.datetime.utcfromtimestamp(int(data["dt"]))
            hour_taken = time_taken.hour + get_offset_from_utc_to_local()
            minute_taken = time_taken.minute
            print('Data taken at ' + f'{hour_taken:0>2}' + ':' + f'{minute_taken:0>2}')
            wind_data = extract_wind_from_weather_api_response(data)
            speed_data = wind_data[1]
            print(f'New Speed: {speed_data} mps')
            deg_data = round(wind_data[0])
            #deg_data = random.randrange(0, 360, 1)
            deg_new = convert_degree_to_unit(deg_data)
            print(f'New Direction Degree: {deg_data} degrees')
            print(f'New Direction Unit: {deg_new} units')
            if deg_new > deg_curr:
                diff = deg_new - deg_curr
                steps(-diff)
                deg_curr = deg_curr + diff
            elif deg_new < deg_curr:
                diff = deg_curr - deg_new
                steps(diff)
                deg_curr = deg_curr - diff
            print(f'Current Direction Degree: {convert_unit_to_degree(deg_curr)}')
            print(f'Current Direction Unit: {deg_curr}')
            time.sleep(60)
            print('~')
    except KeyboardInterrupt:
        if deg_curr < 1024:
            steps(deg_curr)
        else:
            steps(-(2048 - deg_curr))

if __name__ == '__main__':
    main()

#if __name__ == '__main__' :
#	hasRun=False
#while not hasRun:
#	steps(256)
#	hasRun=True
