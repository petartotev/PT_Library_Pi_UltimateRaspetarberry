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

def KeypadRead(cols,rows):
    for r in rows:
        r.value(0)
        result=[cols[0].value(),cols[1].value(),cols[2].value(),cols[3].value()]
        if min(result)==0:
            key=key_map[int(rows.index(r))][int(result.index(0))]
            r.value(1) # manages key keept pressed
            return(key)
        r.value(1)

passwordIsCorrect = False
attemptsCount = 3

password = "ACDC666"

############### LED ###############

red = LED(16)

def ledToggle():
    red.on()

try:
    for x in range(0,attemptsCount):
        print("Enter password:")
        attempt=""
        while True:
            key=KeypadRead(col_list, row_list)
            if key != None and str(key) == "*":
                if (attempt == password):
                    print()
                    print("Password is correct. Let there be light! Red on!")
                    passwordIsCorrect=True
                    break
                else:
                    print()
                    print(f'Password is wrong! {attemptsCount - x - 1} attempts left.')
                    utime.sleep(1)
                    break
            elif key != None and str(key) != "*":
                attempt=attempt+str(key)
                print(str(key),end="")
                utime.sleep(0.3)
            utime.sleep(0.2)
        if (passwordIsCorrect):
            break
    if not passwordIsCorrect:
        print(f'{attemptsCount} unsuccessful attempts. Access forbidden!')
    else:
        ledToggle()
except KeyboardInterrupt:
    red.off()
    print("Keyboard Interrupt. Program exit 0.")