"""Python script plays a MP3 greeting when a PIR sensor scans any movement"""

import time
import datetime
import random
import os
from gtts import gTTS
from gpiozero import LED, MotionSensor

led_red = LED(17)
pir = MotionSensor(4)

greetings = [
    'hello_there',
    'hey_sexy',
    'what_up_yo',
    'speak_of_the_devil',
    'welcome_georgous',
    'nice_to_see_you_here',
    'welcome_back_sailor',
    'hey_hey_hey',
    'whats_new_pussycat',
    'how_is_it_going']

def blink_red_light():
    """Blink Red Light"""
    led_red.on()
    time.sleep(1)
    led_red.off()
    time.sleep(1)

def play_mp3_file(file_path):
    """Play MP3 File"""
    os.system(f'omxplayer -p -o hdmi {file_path}')

def get_random_greeting_mp3_file_path():
    """Get Random Greeting Mp3 File Path"""
    random_song = random.choice(greetings)
    return '/home/pi/Desktop/greetings/' + random_song

def generate_mp3_file_from_string(string, directory, file_name):
    """Generate MP3 File From String"""
    if directory[-1] != "/":
        directory = directory + "/"
    if ".mp3" not in file_name:
        file_name = file_name + ".mp3"
    mp3_file_path = f'{directory}{file_name}'
    def_lang = 'en'
    my_obj = gTTS(text = string, lang = def_lang, slow = False)
    my_obj.save(mp3_file_path)
    return mp3_file_path

def generate_mp3_files_from_greetings():
    """Generate MP3 Files From Greetings"""
    for greeting in greetings:
        generate_mp3_file_from_string(greeting, '/home/pi/Desktop/', greeting + '.mp3')

if __name__ == "__main__":
    try:
        #generate_mp3_files_from_greetings()
        led_red.off()
        while True:
            pir.wait_for_motion()
            file_path = get_random_greeting_mp3_file_path() + '.mp3'
            print(f'{datetime.datetime.now()} | An object is moving!!! {file_path} is on.')
            blink_red_light()
            play_mp3_file(file_path)
            pir.wait_for_no_motion()
            print(f'{datetime.datetime.now()} | No movement in the house...')
            led_red.off()
    except KeyboardInterrupt:
        led_red.off()
