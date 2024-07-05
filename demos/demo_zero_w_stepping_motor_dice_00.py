"""Python script implements Stepping Motor Dice"""

import time
import random
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

StepPins = [24,25,8,7]

for pin in StepPins:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, False)

WAIT_TIME = 0.001

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

def steps(nb):
    """Steps"""
    step_counter = 0
    if nb < 0:
        sign = -1
    else:
        sign = 1
    nb = sign * nb * 2 # times 2 because half-step
    print(f'nbsteps {nb} and sign {sign}')
    for i in range(nb):
        for my_pin in range(4):
            xpin = StepPins[my_pin]
            if Seq[step_counter][my_pin]!=0:
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)
        step_counter += sign
        # If we reach the end of the sequence => start again
        if step_counter == STEP_COUNT:
            step_counter = 0
        if step_counter < 0:
            step_counter = STEP_COUNT-1
        # Wait before moving on
        time.sleep(WAIT_TIME)

listDirections = [-1, 1]
listRotationCycles = [1, 2, 3]

for x in range(5):
    direction = random.choice(listDirections)
    randomRotationCycle = random.choice(listRotationCycles)
    randomRotation = random.randrange(0, 2048, 1)
    if __name__ == '__main__' :
        HAS_RUN = False
    while not HAS_RUN:
        # steps(nbStepsPerRev) # parcourt un tour dans le sens horaire
        # time.sleep(1)
        #steps(-nbStepsPerRev) # parcourt un tour dans le sens anti-horaire
        steps((direction * randomRotationCycle * 2048) + (direction * randomRotation))
        time.sleep(3)
        HAS_RUN = True

# 0	0	.
# 64	11.25	A
# 128	22.5	B
# 192	33.75	C
# 256	45	D
# 320	56.25	E
# 384	67.5	F
# 448	78.75	G
# 512	90	H
# 576	101.25	I
# 640	112.5	J
# 704	123.75	K
# 768	135	L
# 832	146.25	M
# 896	157.5	N
# 960	168.75	O
# 1025	180	P
# 1088	191.25	Q
# 1152	202.5	R
# 1216	213.75	S
# 1280	225	T
# 1344	236.25	U
# 1408	247.5	V
# 1472	258.75	W
# 1536	270	X
# 1600	281.25	Y
# 1664	292.5	Z
# 1728	303.75	0
# 1792	315	1
# 1856	326.25	2
# 1920	337.5	3
# 1984	348.75	4
# 2048	360
