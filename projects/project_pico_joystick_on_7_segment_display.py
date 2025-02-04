# https://www.tomshardware.com/how-to/raspberry-pi-pico-joystick
# https://electrocredible.com/7-segment-display-with-raspberry-pi-pico/

from machine import Pin, ADC
import utime

xAxis = ADC(Pin(27))
yAxis = ADC(Pin(26))
button = Pin(16,Pin.IN, Pin.PULL_UP)

#GPIO pins for 7-segment display segments (a-g)
segments = [
    machine.Pin(8, machine.Pin.OUT),
    machine.Pin(9, machine.Pin.OUT),
    machine.Pin(10, machine.Pin.OUT),
    machine.Pin(11, machine.Pin.OUT),
    machine.Pin(12, machine.Pin.OUT),
    machine.Pin(13, machine.Pin.OUT),
    machine.Pin(14, machine.Pin.OUT)
]

if __name__ == "__main__":
    try:
        while True:
            xValue = xAxis.read_u16()
            yValue = yAxis.read_u16()
            buttonValue = button.value()
            xStatus = "middle"
            yStatus = "middle"
            segments[1].value(1)
            buttonStatus = "not pressed"
            if xValue <= 600:
                xStatus = "left"
                if yValue < 60000:
                    segments[3].value(0)
                if yValue > 600:
                    segments[4].value(0)
            elif xValue >= 60000:
                xStatus = "right"
                if yValue < 60000:
                    segments[5].value(0)
                if yValue > 600:
                    segments[6].value(0)
            else:
                segments[3].value(1)
                segments[4].value(1)
                segments[5].value(1)
                segments[6].value(1)
            if yValue <= 600:
                yStatus = "up"
                segments[0].value(0)
                segments[4].value(1)
                segments[6].value(1)
            elif yValue >= 60000:
                yStatus = "down"
                segments[2].value(0)
                segments[3].value(1)
                segments[5].value(1)
            else:
                segments[0].value(1)
                segments[2].value(1)
            if buttonValue == 0:
                buttonStatus = "pressed"
                segments[1].value(0)
            print("X: " + xStatus + ", Y: " + yStatus + " -- button " + buttonStatus)
            utime.sleep(0.1)
    except KeyboardInterrupt:
        print("Exit...")
    except:
        print("Error!")
