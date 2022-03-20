import sys
sys.path.append("../libraries")
import piLibCamera
import datetime
from time import sleep

def getDirectory(type):
	if type == 'photo':
		return "/home/pi/Desktop/MyDocuments/MyPhotos/"
	elif type == 'video':
		return "/home/pi/Desktop/MyDocuments/MyVideos"
	else:
		raise ValueError('Path input is invalid!')

piLibCamera.takeShot(getDirectory("photo"))
sleep(5)
piLibCamera.takeShot(getDirectory("photo"), 600, 600)
sleep(5)
piLibCamera.takeShotPerMinute(getDirectory("photo"), 3)
sleep(5)
piLibCamera.takeShotPerMinute(getDirectory("photo"), 3, 300, 900)
sleep(5)
piLibCamera.takeVideo(getDirectory("video"), 20)
sleep(5)
piLibCamera.takeVideo(getDirectory("video"), 10, 300, 300)
sleep(5)
piLibCamera.takeShot(getDirectory("wrong"))
