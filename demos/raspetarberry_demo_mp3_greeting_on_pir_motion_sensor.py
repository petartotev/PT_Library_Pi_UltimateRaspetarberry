import time
import datetime
from gpiozero import LED, MotionSensor
from gtts import gTTS
import os
import random

led_red = LED(17)
pir = MotionSensor(4)

greetings = ['hello_there', 'hey_sexy', 'what_up_yo', 'speak_of_the_devil', 'welcome_georgous', 'nice_to_see_you_here', 'welcome_back_sailor', 'hey_hey_hey', 'whats_new_pussycat', 'how_is_it_going']

def blinkRedLight():
    led_red.on()
    time.sleep(1)
    led_red.off()
    time.sleep(1)

def playMp3File(filePath):
    os.system(f'omxplayer -p -o hdmi {filePath}')

def getRandomGreetingMp3FilePath():
    randomSong = random.choice(greetings)
    return '/home/pi/Desktop/greetings/' + randomSong

def generateMp3FileFromString(string, directory, fileName):
    if (directory[-1] != "/"):
        directory = directory + "/"
    if (".mp3" not in fileName):
        fileName = fileName + ".mp3"
    filePath = f'{directory}{fileName}'
    defLang = 'en'
    myObj = gTTS(text = string, lang = defLang, slow = False)
    myObj.save(filePath)
    return filePath

def generateMp3FilesFromGreetings():
    for greeting in greetings:
        generateMp3FileFromString(greeting, '/home/pi/Desktop/', greeting + '.mp3')

try:
    #generateMp3FilesFromGreetings()
    led_red.off()
    while True:
        pir.wait_for_motion()
        filepath = getRandomGreetingMp3FilePath() + '.mp3'
        print(f'{datetime.datetime.now()} | An object is moving!!! {filepath} is on.')
        blinkRedLight()
        playMp3File(filepath)
        pir.wait_for_no_motion()
        print(f'{datetime.datetime.now()} | No movement in the house...')
        led_red.off()
except KeyboardInterrupt:
    led_red.off()
