# Name this file mydot.py

# DEMO 1 (Single button):
#from bluedot import BlueDot
#bd = BlueDot()
#bd.wait_for_press()
#print("You pressed!")

# DEMO 2 (Joystick):
from bluedot import BlueDot
from signal import pause
import time
import RPi.GPIO as io

io.setmode(io.BCM)
led_up = 23
led_down = 24
led_left = 25
led_right = 8
led_fire = 7

io.setup(led_up, io.OUT)
io.setup(led_down, io.OUT)
io.setup(led_left, io.OUT)
io.setup(led_right, io.OUT)
io.setup(led_fire, io.OUT)

def turn_off_lights():
    io.output(led_up, False)
    io.output(led_down, False)
    io.output(led_left, False)
    io.output(led_right, False)
    io.output(led_fire, False)

def dpad(pos):
    if pos.top:
        print("up")
        io.output(led_up, True)
        time.sleep(0.1)
        io.output(led_up, False)
    elif pos.bottom:
        print("bottom")
        io.output(led_down, True)
        time.sleep(0.1)
        io.output(led_down, False)
    elif pos.left:
        print("left")
        io.output(led_left, True)
        time.sleep(0.1)
        io.output(led_left, False)
    elif pos.right:
        print("right")
        io.output(led_right, True)
        time.sleep(0.1)
        io.output(led_right, False)
    elif pos.middle:
        print("fire!")
        io.output(led_fire, True)
        time.sleep(0.1)
        io.output(led_fire, False)
        
turn_off_lights()
bd = BlueDot()
bd.when_pressed = dpad

pause()