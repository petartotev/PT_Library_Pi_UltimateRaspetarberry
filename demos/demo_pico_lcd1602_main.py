from machine import Pin, I2C
from time import sleep
from lcd1602 import LCD1602

# Initialize I2C (Pins GP0=SDA, GP1=SCL, 100kHz speed)
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)

# Create LCD object
lcd = LCD1602(i2c, addr=0x27)  # 0x27 is the default I2C address

# Display message
lcd.clear()
lcd.print("Hello, World!")
lcd.setCursor(0, 1)  # Move to second line
lcd.print("Raspberry Pico")

# Keep text on screen
while True:
    pass
