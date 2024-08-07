""""Demo uses Active Buzzer from FreeNove kit"""

import time
from machine import Pin

button = Pin(3, Pin.IN, Pin.PULL_UP)
buzzer = Pin(11, Pin.OUT)

while True:
    if button.value() == 0:
        print("Button pressed!")
        buzzer.value(1)
        time.sleep(0.1)
    else:
        buzzer.value(0)
