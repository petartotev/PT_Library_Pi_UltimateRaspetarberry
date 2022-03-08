import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

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

if __name__ == '__main__' :
    hasRun=False
    while not hasRun:
            # steps(nbStepsPerRev) # parcourt un tour dans le sens horaire
            # time.sleep(1)
            #steps(-nbStepsPerRev) # parcourt un tour dans le sens anti-horaire
            steps(2048)
            steps(-2048)
            steps(512)
            steps(-512)
            time.sleep(1)
            hasRun=True
    print("Stop motor")
    for pin in StepPins:
            GPIO.output(pin, False)

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


