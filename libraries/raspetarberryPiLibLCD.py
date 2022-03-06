import time
from rpi_lcd import LCD

screen = LCD()

# ████████████████ Line 1 is 16 characters
# ████████████████ Line 2 is 16 characters

def displayTest():
	screen.text(f'Test on Line 1', 1)
	screen.text(f'Test on Line 2', 2)
	time.sleep(5)
	screen.clear()
