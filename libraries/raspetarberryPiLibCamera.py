from picamera import PiCamera
from time import sleep
import datetime
import keyboard

timePreview = 3

msgShotTaken = f'Shot taken!'
msgVideoTaken = f'Video taken!'

camera = PiCamera()
camera.resolution = (1920, 1080)

def getDateNowString():
	result = str(datetime.datetime.now())
	result = result.replace(" ", 'T')
	result = result.replace(":", '')
	result = result.replace("-", '')
	result = result[0:(len(result) - 7)]
	return result

def getFilePathNow(directory, type = "photo"):
	if (directory[-1] != "/"):
		directory = directory + "/"
	if (type == "video"):
		return directory + "video" + getDateNowString() + ".h264"
	elif (type == "photo"):
		return directory + "photo" + getDateNowString() + ".jpg"
	else:
		raise ValueError("Wrong shoot type!")

def setResolution(width, height):
	camera.resolution = (int(width), int(height))

def takeShot(directory, width = 1920, height = 1280):
	setResolution(width, height)
	camera.start_preview()
	sleep(timePreview)
	camera.capture(getFilePathNow(directory))
	camera.stop_preview()
	print(getDateNowString() + " | " + msgShotTaken)

def takeShotPerMinute(directory, count = 60, width = 1920, height = 1280):
	for m in range(count):
		takeShot(directory, width, height)
		sleep(60 - timePreview)

def takeShotPerDay(directory, count = 365, width = 1920, height = 1280):
	for d in range(count):
		takeShot(directory, width, height)
		sleep((60 * 60 * 24) - timePreview)

def takeVideo(directory, duration = 60, width = 1920, height = 1080):
	setResolution(width, height)
	camera.start_recording(getFilePathNow(directory, "video"))
	camera.wait_recording(duration)
	camera.stop_recording()
	print(getDateNowString() + " | " + msgVideoTaken)
