""""Python Script implements keypad password key switch mechanism"""

from machine import Pin
import utime
from picozero import LED

############### Keypad ###############

col_list=[6,7,8,9]
row_list=[10,11,12,13]
key_map=[["D","#","0","*"],["C","9","8","7"],["B","6","5","4"],["A","3","2","1"]]

for x in range(0,4):
    row_list[x]=Pin(row_list[x], Pin.OUT)
    row_list[x].value(1)
    col_list[x] = Pin(col_list[x], Pin.IN, Pin.PULL_UP)

def read_keypad(cols,rows):
    """Read Keypad"""
    for r in rows:
        r.value(0)
        result=[cols[0].value(),cols[1].value(),cols[2].value(),cols[3].value()]
        if min(result)==0:
            key=key_map[int(rows.index(r))][int(result.index(0))]
            r.value(1) # manages key keept pressed
            return key
        r.value(1)

PASSWORD = "ACDC666"
PASSWORD_IS_CORRECT = False
ATTEMPTS_COUNT = 3

############### LED ###############

red = LED(16)

def led_toggle():
    """Turn Red LED on"""
    red.on()

############### MAIN ###############

if __name__ == "__main__":
    try:
        for x in range(0, ATTEMPTS_COUNT):
            print("Enter password:")
            ATTEMPT=""
            while True:
                key=read_keypad(col_list, row_list)
                if key is not None and str(key) == "*":
                    if ATTEMPT == PASSWORD:
                        print()
                        print("Password is correct. Let there be light! Red on!")
                        PASSWORD_IS_CORRECT=True
                        break
                    print()
                    print(f'Password is wrong! {ATTEMPTS_COUNT - x - 1} attempts left.')
                    utime.sleep(1)
                elif key is not None and str(key) != "*":
                    ATTEMPT=ATTEMPT+str(key)
                    print(str(key),end="")
                    utime.sleep(0.3)
                utime.sleep(0.2)
            if PASSWORD_IS_CORRECT:
                break
        if not PASSWORD_IS_CORRECT:
            print(f'{ATTEMPTS_COUNT} unsuccessful attempts. Access forbidden!')
        else:
            led_toggle()
    except KeyboardInterrupt:
        red.off()
        print("Keyboard Interrupt. Program exit 0.")
