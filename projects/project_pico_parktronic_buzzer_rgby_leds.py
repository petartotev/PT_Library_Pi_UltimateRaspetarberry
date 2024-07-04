"""Pico Parktronic"""

from machine import Pin
import utime
from picozero import LED

buzzer = Pin(6, Pin.OUT)
buzzer2 = Pin(14, Pin.OUT)

redLed = LED(13)
yellowLed = LED(12)
greenLed = LED(11)
blueLed = LED(10)

trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)

def set_buzzers(val1, val2):
    """Set buzzers"""
    buzzer.value(val1)
    buzzer2.value(val2)

def turn_leds_off():
    """Turn leds off"""
    blueLed.off()
    greenLed.off()
    yellowLed.off()
    redLed.off()

def turn_on_leds_in_sequence(count = 5):
    """Turns all 4 LEDs on sequentially in R>G>B>Y order"""
    for _ in range(0,count):
        utime.sleep_us(0.25)
        redLed.on()
        utime.sleep_us(0.25)
        redLed.off()
        greenLed.on()
        utime.sleep_us(0.25)
        greenLed.off()
        blueLed.on()
        utime.sleep_us(0.25)
        blueLed.off()
        yellowLed.on()
        utime.sleep_us(0.25)
        yellowLed.off()

def turn_led_on_based_on_distance(dist):
    """Turn leds on based on distance"""
    turn_leds_off()
    if dist <= 30:
        redLed.on()
        if dist <= 10:
            set_buzzers(1,1)
        elif 10 < dist < 20:
            set_buzzers(1,0)
        else:
            set_buzzers(0,0)
    elif 30 < dist <= 60:
        yellowLed.on()
        set_buzzers(0,0)
    elif 60 < dist <= 90:
        greenLed.on()
        set_buzzers(0,0)
    else:
        blueLed.on()
        set_buzzers(0,0)

def ultra():
    """Ultra"""
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2
    turn_led_on_based_on_distance(distance)
    print("The distance from object is ",distance,"cm")

def main():
    """Main program"""
    turn_leds_off()
    while True:
        ultra()
        utime.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        turn_leds_off()
        set_buzzers(0,0)
        print("Keyboard Interrupt. Program exit 0.")
