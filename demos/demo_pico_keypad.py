from machine import Pin
import utime

matrix_keys = [['1', '2', '3', 'A'],
               ['4', '5', '6', 'B'],
               ['7', '8', '9', 'C'],
               ['*', '0', '#', 'D']]

# PINs according to schematic - Change the pins to match with your connections
keypad_rows = [9,8,7,6]
keypad_columns = [5,4,3,2]

# Create two empty lists to set up pins ( Rows output and columns input )
col_pins = []
row_pins = []

# Loop to assign GPIO pins and setup input and outputs
for x in range(0,4):
    row_pins.append(Pin(keypad_rows[x], Pin.OUT))
    row_pins[x].value(1)
    col_pins.append(Pin(keypad_columns[x], Pin.IN, Pin.PULL_DOWN))
    col_pins[x].value(0)
    
def scan_keypad():  
    for row in range(4):
        for col in range(4):
            row_pins[row].high()
            key = None
            
            if col_pins[col].value() == 1:
                #print("You have pressed:", matrix_keys[row][col])
                print("ASCII Value:", ord(matrix_keys[row][col]))
                #key_press = matrix_keys[row][col]
                utime.sleep(0.5)
                    
        row_pins[row].low()


if __name__ == "__main__":
    try:
        print("Enter input and press '#' as enter!")
        while True:
            scan_keypad()
    except KeyboardInterrupt:
        print("Keyboard interrupt!")
    except Exception as ex:
        print("Unexpected exception!", ex)

