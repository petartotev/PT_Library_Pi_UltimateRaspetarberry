"""Python script implements a Digital Dice using 7-segment display"""

import time
import random
from gpiozero import LEDBoard, OutputDeviceError, LEDCollection, Button

# Class is copied from:
# https://www.stuffaboutcode.com/2016/10/raspberry-pi-7-segment-display-gpiozero.html

class SevenSegmentDisplay(LEDBoard):
    """Seven Segment Display Class"""
    def __init__(self, *pins, **kwargs):
        # 7 segment displays must have 7 or 8 pins
        if len(pins) < 7 or len(pins) > 8:
            raise ValueError('SevenSegmentDisplay must have 7 or 8 pins')
        # Don't allow 7 segments to contain collections
        for pin in pins:
            assert not isinstance(pin, LEDCollection)
        pwm = kwargs.pop('pwm', False)
        active_high = kwargs.pop('active_high', True)
        initial_value = kwargs.pop('initial_value', False)
        if kwargs:
            raise TypeError('unexpected keyword argument: %s' % kwargs.popitem()[0])

        self._layouts = {
            '1': (False, True, True, False, False, False, False),
            '2': (True, True, False, True, True, False, True),
            '3': (True, True, True, True, False, False, True),
            '4': (False, True, True, False, False, True, True),
            '5': (True, False, True, True, False, True, True),
            '6': (True, False, True, True, True, True, True),
            '7': (True, True, True, False, False, False, False),
            '8': (True, True, True, True, True, True, True),
            '9': (True, True, True, True, False, True, True),
            '0': (True, True, True, True, True, True, False),
            'A': (True, True, True, False, True, True, True),
            'B': (False, False, True, True, True, True, True),
            'C': (True, False, False, True, True, True, False),
            'D': (False, True, True, True, True, False, True),
            'E': (True, False, False, True, True, True, True),
            'F': (True, False, False, False, True, True, True),
            'G': (True, False, True, True, True, True, False),
            'H': (False, True, True, False, True, True, True),
            'I': (False, False, False, False, True, True, False),
            'J': (False, True, True, True, True, False, False),
            'K': (True, False, True, False, True, True, True),
            'L': (False, False, False, True, True, True, False),
            'M': (True, False, True, False, True, False, False),
            'N': (True, True, True, False, True, True, False),
            'O': (True, True, True, True, True, True, False),
            'P': (True, True, False, False, True, True, True),
            'Q': (True, True, False, True, False, True, True),
            'R': (True, True, False, False, True, True, False),
            'S': (True, False, True, True, False, True, True),
            'T': (False, False, False, True, True, True, True),
            'U': (False, False, True, True, True, False, False),
            'V': (False, True, True, True, True, True, False),
            'W': (False, True, False, True, False, True, False),
            'X': (False, True, True, False, True, True, True),
            'Y': (False, True, True, True, False, True, True),
            'Z': (True, True, False, True, True, False, True),
            '-': (False, False, False, False, False, False, True),
            ' ': (False, False, False, False, False, False, False),
            '=': (False, False, False, True, False, False, True)
        }

        super(SevenSegmentDisplay, self).__init__(*pins, pwm=pwm, active_high=active_high, initial_value=initial_value)

    def display(self, char):
        """Display"""
        char = str(char).upper()
        if len(char) > 1:
            raise ValueError('only a single character can be displayed')
        if char not in self._layouts:
            raise ValueError('there is no layout for character - %s' % char)
        layout = self._layouts[char]
        for led in range(7):
            self[led].value = layout[led]

    def display_hex(self, hexnumber):
        """Display Hex"""
        self.display(hex(hexnumber)[2:])

    @property
    def decimal_point(self):
        """Get Decimal Point"""
        # does the 7seg display have a decimal point (i.e pin 8)
        if len(self) > 7:
            return self[7].value
        raise OutputDeviceError('there is no 8th pin for the decimal point')

    @decimal_point.setter
    def decimal_point(self, value):
        """Set Decimal Point"""
        if len(self) > 7:
            self[7].value = value
        else:
            raise OutputDeviceError('there is no 8th pin for the decimal point')    

    def set_char_layout(self, char, layout):
        """Set Char Layout"""
        char = str(char).upper()
        if len(char) != 1:
            raise ValueError('only a single character can be used in a layout')
        if len(layout) != 7:
            raise ValueError('a character layout must have 7 segments')
        self._layouts[char] = layout

# Demo code starts from here
seven_seg = SevenSegmentDisplay(20, 21, 6, 22, 27, 18, 15, 13, active_high=False)

btnG = Button(26)

listNums = [1, 2, 3, 4, 5, 6]

try:
    while True:
        if btnG.is_pressed:
            randomNum = random.choice(listNums)
            seven_seg.display(str(randomNum))
            time.sleep(5)
            seven_seg.display(" ")
except KeyboardInterrupt:
    seven_seg.display(" ")
finally:
    seven_seg.display(" ")
