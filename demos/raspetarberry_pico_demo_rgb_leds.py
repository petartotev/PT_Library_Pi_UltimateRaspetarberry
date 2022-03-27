import utime
from machine import Pin, PWM

led_red = Pin(21)
led_green = Pin(20)
led_blue = Pin(19)
led_yellow = Pin(18)
pwm_red = PWM(led_red)
pwm_green = PWM(led_green)
pwm_blue = PWM(led_blue)
pwm_yellow = PWM(led_yellow)
pwm_red.freq(1000)
pwm_green.freq(1000)
pwm_blue.freq(1000)
pwm_yellow.freq(1000)


def blink():
    pwm_red.duty_u16(255 * 255)
    utime.sleep(1)
    pwm_red.duty_u16(0)
    pwm_green.duty_u16(255 * 255)
    utime.sleep(1)
    pwm_green.duty_u16(0)
    pwm_blue.duty_u16(255 * 255)
    utime.sleep(1)
    pwm_blue.duty_u16(0)
    pwm_yellow.duty_u16(255 * 255)
    utime.sleep(1)
    pwm_yellow.duty_u16(0)


while(True):
	blink()


# import utime
# >>> from machine import Pin, PWM
# >>> led_red = Pin(21)
# >>> led_green = Pin(20)
# >>> led_blue = Pin(19)
# >>> led_yellow = Pin(18)
# >>> pwm_red = PWM(led_red)
# >>> pwm_green = PWM(led_green)
# >>> pwm_blue = PWM(led_blue)
# >>> pwm_yellow = PWM(led_yellow)
# >>> pwm_red.freq(1000)
# >>> pwm_green.freq(1000)
# >>> pwm_blue.freq(1000)
# >>> pwm_yellow.freq(1000)
# >>> pwm_red.duty_u16(255)
# >>> pwm_red.duty_u16(0)
# >>> pwm_red.duty_u16(500)
# >>> pwm_red.duty_u16(0)
# >>> pwm_red.duty_u16(255 * 255)
# >>> pwm_green.duty_u16(255 * 255)
# >>> pwm_blue.duty_u16(255 * 255)
# >>> pwm_yellow.duty_u16(255 * 255)
# >>> pwm_red.duty_u16(0)
# >>> pwm_green.duty_u16(0)
# >>> pwm_blue.duty_u16(0)
# >>> pwm_yellow.duty_u16(0)
# >>> import keyboard
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# ImportError: no module named 'keyboard'
# >>> from machine import keyboard
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# ImportError: can't import name keyboard
# >>> from machine import keyboard
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# ImportError: can't import name keyboard
# >>> import keyboard
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# ImportError: no module named 'keyboard'
# >>> def play_led_sequence(sequence):
# ...     for letter in sequence:
# ...         if (letter == "R" or letter == "r"):
# ...             pwm_red.duty_u16(255 * 255)
# ...             if (letter == "G" or letter == "g"):
# ...                 
# >>> 
# >>> def play_led_sequence(sequence):
# ...     for letter in sequence:
# ...         if (letter == "R" or letter == "r"):
# ...             pwm_red.duty_u16(255 * 255)
# ...             
# ...             if (letter == "G" or letter == "g"):
# ...                 
# >>> def play_led_sequence(sequence):
# ...     for letter in sequence:
# ...         if (letter == "R" or letter == "r"):
# ...             pwm_red.duty_u16(255 * 255)
# ...             
# ...             
# ... 
# >>> 