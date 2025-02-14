# PT_Library_Pi_UltimateRaspetarberry

# General Information
PT_Library_Pi_UltimateRaspetarberry is a public repo which contains a personal collection of libraries, demos, projects and diagrams for Raspberry Pi.

![cover](demos/demo_zero_w_keypad_lcd1602.jpg)

# Contents
- [Setup](#setup)
	- [Setup Pico](#setup-pico)
	- [Setup Pico W](#setup-pico-w)
	- [Setup Zero W](#setup-zero-w)
	- [Setup Zero 2W](#setup-zero-2w)
	- [Setup Pi 4](#setup-pi-4)
- [Projects](#projects)
	- [Project Pico W Weather Station](#project-pico-w-weather-station)
	- [Project Pico Game Boy](#project-pico-game-boy)
	- [Project Pico Parktronic](#project-pico-parktronic)
- [Projects Old](#projects-old)
	- [NASA API Wallpaper](#nasa-api-wallpaper)
	- [Game Blinking RGBY LEDs](#game-blinking-rgby-leds-remembergby)
	- [Parktronic Buzzer](#parktronic-buzzer)
	- [Temperature on LCD Screen](#temperature-on-lcd-screen)
	- [Dice 7-Segment](#dice-7-segment)
	- [MP3 Greeting on Movement](#mp3-greeting-on-movement)
	- [Windcock Stepping Motor](#windcock-stepping-motor)
- [Demos](#demos)
	- [Buzzer Active](#buzzer-active)
	- [Dust Sensor](#dust-sensor)
	- [Keypad + Key Switch](#keypad--key-switch)
	- [RGB LEDs](#rgb-leds)
	- [WiFi Pico](#wifi-pico)
	- [Camera](#camera)
	- [Keypad + LCD](#keypad--lcd)
	- [Temperature Sensor DHT11](#temperature-sensor-dht11)
	- [Stepping Motor](#stepping-motor)
- [Sensors](#sensors)
	- [Dust Sensor Sharp GP2Y1010AU0F](#dust-sensor-sharp-gp2y1010au0f)
	- [LCD1602 RGB Module](#lcd1602-rgb-module)
- [Technologies](#technologies)
- [Known Issues](#known-issues)
	- [Raspberry Pi Inaccurate Clock](#raspberry-pi-clock-inaccurate)
   	- [Raspberry Pi Boot Issues due to SD Card](#raspberry-pi-boot-issues-due-to-sd-card)
- [Links](#links)

# Setup
## Setup Pico

![pinout](./res/pinout_raspberry_pico.jpg)

## Setup Pico W

Install the latest MicroPython firmware for Pico W:
- Download the latest UF2 firmware for Pico W from https://micropython.org/download/RPI_PICO_W/.
- Plug in your Pico W while holding the BOOTSEL button.
- It will appear as a drive on your computer.
- Drag and drop the .uf2 file you downloaded onto it.
- The board will reboot into MicroPython.

## Setup Zero W

![pinout](./res/pinout_raspberry_zero.jpg)

## Setup Zero 2W

## Setup Pi 4

![pinout](./res/pinout_raspberry_pi_4.jpg)

# Projects

## Project Pico W Weather Station

`./projects/project_pico_w_weather_station/src/main.py`

### Encrypt Secrets.py with Base-64

1. Encode Your Secrets (Run Python on Your Computer)

```
import base64

# Replace with your actual secrets
ssid = "YOUR_WIFI_SSID"
password = "YOUR_WIFI_PASSWORD"
nasa_api_key = "YOUR_NASA_API_KEY"

encoded_ssid = base64.b64encode(ssid.encode()).decode()
encoded_password = base64.b64encode(password.encode()).decode()
encoded_api_key = base64.b64encode(nasa_api_key.encode()).decode()

print(f"SSID: {encoded_ssid}")
print(f"PASSWORD: {encoded_password}")
print(f"NASA_API_KEY: {encoded_api_key}")
```

2. Update Your secrets.py on the Pico

```
import base64

SSID = base64.b64decode('LUTVUl7XSUZJX2NTZUQ=').decode()
PASSWORD = base64.b64decode('WU1VUl3XLOVEX1BBB1NXT1JE').decode()
NASA_API_KEY = base64.b64decode('QUZDMTIzVASA').decode()
```

3. Keep main.py Unchanged

## Project Pico Game Boy

`./projects/project_pico_game_boy/src/main.py`

## Project Pico Parktronic

`./projects/project_pico_parktronic/src/main.py`

# Projects Old
## NASA API Wallpaper
## Game Blinking RGBY LEDs "RemembeRGBY"
## Parktronic Buzzer
## Temperature on LCD Screen
## Dice 7-Segment
## MP3 Greeting on Movement
## Windcock Stepping Motor

# Demos
## Buzzer Active
## Dust Sensor
## Keypad + Key Switch
## RGB LEDs
## WiFi Pico
## Camera
## Keypad + LCD
## Temperature Sensor DHT11
## Stepping Motor

# Sensors

## Dust Sensor Sharp GP2Y1010AU0F
- https://erelement.com/shop/sharp-gp2y1010au0f/
- https://www.waveshare.com/dust-sensor.htm

## LCD1602 RGB Module
- https://www.waveshare.com/lcd1602-rgb-module.htm

# Technologies
- import multiprocessing (with lock)
	- demos/raspetarberryPiDemoLCD1602AndTempSensorDHT11_01.py

# Known Issues

## Raspberry Pi Clock Inaccurate

https://stackoverflow.com/questions/71868313/how-to-sync-raspberry-pi-system-clock

1. Connect Raspberry Pi Zero W to the Internet
2. Execute the following command in the Linux Terminal:
```
sudo date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z"
```
3. ✅ SUCCESS: RPi Clock gets set just fine!

## Raspberry Pi Boot Issues due to SD Card

⚠️ ERROR: When Raspberry Pi gets booted, the following series of errors occur in Terminal:

```
mmc0: timeout waiting for hardware interrupt.
blk_update_request: I/O error, dev mmcblk0, sector 1492446 op 0x0:(READ) flags 0x0 phys_seg 1 prio class 0
systemd[1]: Caught <BUS>, core dump failed (child 89, code=killed, status=7/BUS).
systemd[1]: Freezing execution.
systemd-journalid[87]: Failed to send READY=1 notification message: Connection refused
systemd-journalid[87]: Failed to send READY=1 notification message: Transport endpoint is not connected
```

✅ SUCCESS: Take the SD card out of your Raspberry Pi, then plug it in again to get things right!

## Raspberry Pico Not Read When Connected With HDMI Cable

Use Data cable, not Charging cable!

# Links
- [Good article on Multiprocessing](https://analyticsindiamag.com/run-python-code-in-parallel-using-multiprocessing/#:~:text=Multiprocessing%20in%20Python%20enables%20the,run%20tasks%2Fprocesses%20in%20parallel.&text=Multiprocessing%20enables%20the%20computer%20to,involve%20a%20lot%20of%20computation.)  
- [Stack Overflow article on Multiprocessing with Lock](https://stackoverflow.com/questions/28267972/python-multiprocessing-locks)  
- [Article on 7-Segment-Display implementation](https://www.stuffaboutcode.com/2016/10/raspberry-pi-7-segment-display-gpiozero.html)  
- [Article on Keypad implementation](https://www.digikey.bg/en/maker/blogs/2021/how-to-connect-a-keypad-to-a-raspberry-pi)  
- [Article on Stepping Motor](https://www.aranacorp.com/en/control-a-stepper-with-raspberrypi/)  
- [Pico Not Connected to PC due to Cable](https://forums.raspberrypi.com/viewtopic.php?t=308412)
- [NASA Wallpaper Fit](https://forum.lxde.org/viewtopic.php?t=31984)
- [NASA Wallpaper Fit 2](https://stackoverflow.com/questions/45873124/pcmanfm-set-wallpaper-fails-on-raspbian-stretch-in-cron)