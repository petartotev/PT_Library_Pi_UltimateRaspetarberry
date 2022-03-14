import time
import RPi.GPIO as GPIO
import random
import requests
import http.client
import geocoder
import json
import credentials
import datetime
import sys

GPIO.setmode(GPIO.BCM)

# STEPPING MOTOR

StepPins = [24,25,8,7]

for pin in StepPins:
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin, False)

WaitTime = 0.001

StepCount1 = 4
Seq1 = []
Seq1 = [i for i in range(0, StepCount1)]
Seq1[0] = [1,0,0,0]
Seq1[1] = [0,1,0,0]
Seq1[2] = [0,0,1,0]
Seq1[3] = [0,0,0,1]

StepCount2 = 8
Seq2 = []
Seq2 = [i for i in range(0, StepCount2)]
Seq2[0] = [1,0,0,0]
Seq2[1] = [1,1,0,0]
Seq2[2] = [0,1,0,0]
Seq2[3] = [0,1,1,0]
Seq2[4] = [0,0,1,0]
Seq2[5] = [0,0,1,1]
Seq2[6] = [0,0,0,1]
Seq2[7] = [1,0,0,1]

Seq = Seq2
StepCount = StepCount2

def steps(nb):
        StepCounter = 0
        if nb<0: sign=-1
        else: sign=1
        nb=sign*nb*2 #times 2 because half-step
        print("nbsteps {} and sign {}".format(nb,sign))
        for i in range(nb):
                for pin in range(4):
                        xpin = StepPins[pin]
                        if Seq[StepCounter][pin]!=0:
                                GPIO.output(xpin, True)
                        else:
                                GPIO.output(xpin, False)
                StepCounter += sign
        # If we reach the end of the sequence
        # start again
                if (StepCounter==StepCount):
                        StepCounter = 0
                if (StepCounter<0):
                        StepCounter = StepCount-1
                # Wait before moving on
                time.sleep(WaitTime)

# OPEN WEATHER API

domainApiIpifyOrg = 'https://api.ipify.org'
domainWeatherApi = 'api.openweathermap.org'
domainWeatherApiKey = credentials.getWeatherApiKey()

def getOffsetFromUtcToLocal():
	now = time.time()
	offset = datetime.datetime.fromtimestamp(now) - datetime.datetime.utcfromtimestamp(now)
	return int(offset.seconds / 3600)

def getWeatherApiResponse(lat, lon, keyWeatherApi):
	urlWeatherApi = f'/data/2.5/weather?lat={lat}&lon={lon}&appid={keyWeatherApi}'
	conn = http.client.HTTPSConnection(domainWeatherApi)
	conn.request("GET", urlWeatherApi)
	response = conn.getresponse()
	data = response.read()
	dataDecoded = data.decode("utf-8")
	return json.loads(dataDecoded)

def getWindDataFromWeatherApiResponse(response):
	windDirection = response["wind"]["deg"]
	windSpeed = response["wind"]["speed"]
	return windDirection, windSpeed

def getTimeFromWeatherApiResponse(response):
	time = response["dt"]

def degreeToUnit(degree):
	return round((2048 * round(degree)) / 360)

def unitToDegree(unit):
	return round((360 * round(unit)) / 2048)

def getLatAndLonByIpAddress():
	ipPublic = requests.get(domainApiIpifyOrg).text
	geo = geocoder.ip(ipPublic)
	lat = geo.latlng[0]
	lon = geo.latlng[1]
	return lat, lon

def getCoordinatesFromRunArgs():
	city = str(sys.argv[1])
	if (city == "CherniVruh"):
		lat = 42.56378836361624
		lon =  23.278416348642256
	elif (city == "Sofia"):
		lat = 42.68232568553703
		lon = 23.335369831287874
	elif (city == "Burgas"):
		lat = 42.493969995866784
		lon = 27.46136420793039
	else:
		response = getLatAndLonByIpAddress()
		lat = response[0]
		lon = response[1]
	return lat, lon

# PROGRAM
def main():
	coords = getCoordinatesFromRunArgs()
	lat = coords[0]
	lon = coords[1]
	degCurr = 0
	print(f'Lat is {lat}, Lon is {lon}.')
	print('~')
	try:
		while(True):
			#print(f'degCurr before update: {degCurr}')
			try:
				data = getWeatherApiResponse(lat, lon, domainWeatherApiKey)
			except KeyboardInterrupt:
				if (degCurr < 1024):
					steps(degCurr)
				else:
					steps(-(2048 - degCurr))
				sys.exit("Keyboard interrupt! Exit!")
			except:
				if (degCurr < 1024):
					steps(degCurr)
				else:
					steps(-(2048 - degCurr))
				degCurr = 0
				print("ERROR: Request to Weather API failed!")
				time.sleep(10)
				continue
			timeTaken = datetime.datetime.utcfromtimestamp(int(data["dt"]))
			hourTaken = timeTaken.hour + getOffsetFromUtcToLocal()
			minuteTaken = timeTaken.minute
			print('Data taken at ' + f'{hourTaken:0>2}' + ':' + f'{minuteTaken:0>2}')
			windData = getWindDataFromWeatherApiResponse(data)
			speedData = windData[1]
			print(f'New Speed: {speedData} mps')
			degData = round(windData[0])
			#degData = random.randrange(0, 360, 1)
			degNew = degreeToUnit(degData)
			print(f'New Direction Degree: {degData} degrees')
			print(f'New Direction Unit: {degNew} units')
			if (degNew > degCurr):
				diff = degNew - degCurr
				steps(-diff)
				degCurr = degCurr + diff
			elif (degNew < degCurr):
				diff = degCurr - degNew
				steps(diff)
				degCurr = degCurr - diff
			print(f'Current Direction Degree: {unitToDegree(degCurr)}')
			print(f'Current Direction Unit: {degCurr}')
			time.sleep(60)
			print('~')
	except KeyboardInterrupt:
		if (degCurr < 1024):
			steps(degCurr)
		else:
			steps(-(2048 - degCurr))

main()

#if __name__ == '__main__' :
#	hasRun=False
#while not hasRun:
#	steps(256)
#	hasRun=True

