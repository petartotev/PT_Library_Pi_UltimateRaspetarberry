"""This is python script that contains a game called RecalLED"""

# Open Thonny IDE > Configure Interpreter > MicroPython (Raspberry Pi Pico) . COM3
# In Thonny > Tools > Manage Packages... > Install picozero from PyPi

from time import sleep
import random
import sys
from machine import Pin
from picozero import LED

redLed = LED(21)
greenLed = LED(20)
blueLed = LED(19)
yellowLed = LED(18)

redBtn = Pin(28, Pin.IN, Pin.PULL_UP)
greenBtn = Pin(27, Pin.IN, Pin.PULL_UP)
blueBtn = Pin(26, Pin.IN, Pin.PULL_UP)
yellowBtn = Pin(22, Pin.IN, Pin.PULL_UP)

GAME_DIFFICULTY = 5
GAME_ROUNDS = 3
GAME_BLINK_DURATION = 1

########## GAME OPTIONS ##########
def set_difficulty():
    """Sets difficulty"""
    print("Set difficulty. Press RED for 5, GREEN for 7, BLUE for 9, YELLOW for 11...")
    while True:
        if redBtn.value() == 0:
            return 5
        if greenBtn.value() == 0:
            return 7
        if blueBtn.value() == 0:
            return 9
        if yellowBtn.value() == 0:
            return 11

def set_rounds():
    """Sets rounds count"""
    print("Set rounds count. Press RED for 3, GREEN for 6, BLUE for 9, YELLOW for 12...")
    while True:
        if redBtn.value() == 0:
            return 3
        if greenBtn.value() == 0:
            return 6
        if blueBtn.value() == 0:
            return 9
        if yellowBtn.value() == 0:
            return 12

def set_blink_duration():
    """Sets blink duration"""
    print("Set LED blink duration. Press RED for 2, GREEN for 1.5, BLUE for 1, YELLOW for 0.5...")
    while True:
        if redBtn.value() == 0:
            return 2
        if greenBtn.value() == 0:
            return 1.5
        if blueBtn.value() == 0:
            return 1
        if yellowBtn.value() == 0:
            return 0.5

########## USER INPUT ##########
def get_user_input():
    """Gets user input"""
    inputs_left = GAME_DIFFICULTY
    input_str=""
    print("Enter your input:")
    while True:
        if inputs_left == 0:
            break
        if redBtn.value() == 0:
            input_str=input_str+"R"
            print("R",end="")
            inputs_left=inputs_left-1
        elif greenBtn.value() == 0:
            input_str=input_str+"G"
            print("G",end="")
            inputs_left=inputs_left-1
        elif blueBtn.value() == 0:
            input_str=input_str+"B"
            print("B",end="")
            inputs_left=inputs_left-1
        elif yellowBtn.value() == 0:
            input_str=input_str+"Y"
            print("Y",end="")
            inputs_left=inputs_left-1
        sleep(0.4)
    print()
    return input_str

def does_user_want_one_more():
    """Returns user input if another game is demanded"""
    print("One more game? Press GREEN for yes and RED for no...")
    while True:
        if redBtn.value() == 0:
            return False
        if greenBtn.value() == 0:
            return True

########## LED ##########
def turn_off_leds():
    """Turns all 4 LEDs off"""
    redLed.off()
    greenLed.off()
    blueLed.off()
    yellowLed.off()

def turn_on_leds_in_sequence(count = 1):
    """Turns all 4 LEDs on sequentially in R>G>B>Y order"""
    for _ in range(0,count):
        sleep(0.25)
        redLed.on()
        sleep(0.25)
        redLed.off()
        greenLed.on()
        sleep(0.25)
        greenLed.off()
        blueLed.on()
        sleep(0.25)
        blueLed.off()
        yellowLed.on()
        sleep(0.25)
        yellowLed.off()

########## MAIN ##########
try:
    while True:
        turn_off_leds()
        turn_on_leds_in_sequence(1)
        print("Welcome to 'RECAL`LED' game!")
        GAME_DIFFICULTY = set_difficulty()
        print(f'Difficulty is {GAME_DIFFICULTY}!')
        sleep(1)
        GAME_ROUNDS = set_rounds()
        print(f'Rounds count is {GAME_ROUNDS}!')
        sleep(1)
        BLINK_DURATION = set_blink_duration()
        print(f'LED blink duration is {GAME_BLINK_DURATION}!')
        sleep(1)
        print("Game is on!")
        RESULT=0
        for rnd in range(0, GAME_ROUNDS):
            SEQUENCE=""
            print(f'Round {rnd + 1}... Go!')
            sleep(5)
            for blink in range(0, GAME_DIFFICULTY):
                value = random.randint(0,3)
                if value == 0:
                    redLed.on()
                    sleep(GAME_BLINK_DURATION)
                    redLed.off()
                    SEQUENCE=SEQUENCE+"R"
                if value == 1:
                    greenLed.on()
                    sleep(GAME_BLINK_DURATION)
                    greenLed.off()
                    SEQUENCE=SEQUENCE+"G"
                if value == 2:
                    blueLed.on()
                    sleep(GAME_BLINK_DURATION)
                    blueLed.off()
                    SEQUENCE=SEQUENCE+"B"
                if value == 3:
                    yellowLed.on()
                    sleep(GAME_BLINK_DURATION)
                    yellowLed.off()
                    SEQUENCE=SEQUENCE+"Y"
                sleep(GAME_BLINK_DURATION)
            INPUT = get_user_input()
            if INPUT == SEQUENCE:
                print("Your input is correct!")
                RESULT=RESULT+1
            else:
                print(f'Wrong! Your input {INPUT} != {SEQUENCE}.')
            print(f'Current result is {RESULT}/{rnd + 1}.')
        print(f'Final result is {RESULT}/{GAME_ROUNDS}.')
        if RESULT == GAME_ROUNDS:
            print("Congratulations! You won!")
            turn_on_leds_in_sequence(3)
        else:
            print("You could do better...")
        sleep(3)
        if not does_user_want_one_more():
            sleep(1)
            print("Goodbye...")
            sleep(1)
            sys.exit()
except KeyboardInterrupt:
    turn_off_leds()
    print("Keyboard Interrupt. Program exit 0.")
