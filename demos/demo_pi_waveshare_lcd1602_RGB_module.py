# Note that you need to unzip ./res/LCD1602-RGB-Module-demo.zip.
# Next, find the ./Raspberry/RGB1602.py file and make sure you have it in the directory of this file!

import RGB1602
import time

lcd=RGB1602.RGB1602(16,2)
lcd.setRGB(64,128,64) # greenish

lcd.setCursor(0,0)
lcd.printout("Hello,")
time.sleep(1)

lcd.setCursor(0,1)
lcd.printout("World!")
time.sleep(3)

lcd.clear()