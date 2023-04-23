'''Windcock Helper'''

import time
import sys
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

try:
    steps(int(sys.argv[1]))
except:
    steps(0)
