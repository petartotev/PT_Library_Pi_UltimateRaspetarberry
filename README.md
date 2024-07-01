# PT_Library_Pi_UltimateRaspetarberry

## General Information
PT_Library_Pi_UltimateRaspetarberry is a public repo which contains a personal collection of libraries, demos and diagrams for Raspberry Pi.

![cover](demos/raspetarberry_demo_keypad_input_on_lcd1602.jpg)

## Contents
- [Folder Structure](#folder-structure)
- [Technologies](#technologies)
- [Known Issues](#known-issues)
	- [Raspberry Pi Inaccurate Clock](#raspberry-pi-clock-inaccurate)
   	- [Raspberry Pi Boot Issues due to SD Card](#raspberry-pi-boot-issues-due-to-sd-card)
- [Links](#links)

## Folder Structure

- /demos - Python scripts that implement the libraries of this repository
- /diagrams - Images that represent personally drawn diagrams of the connections between Pi and gadgets onto a breadboard
- /libraries - Python scripts that wrap outer libraries for easier use of different sensors and other gadgets through the Pi's GPIO

## Technologies
- import multiprocessing (with lock)
	- demos/raspetarberryPiDemoLCD1602AndTempSensorDHT11_01.py

## Known Issues

### Raspberry Pi Clock Inaccurate

https://stackoverflow.com/questions/71868313/how-to-sync-raspberry-pi-system-clock

1. Connect Raspberry Pi Zero W to the Internet
2. Execute the following command in the Linux Terminal:
```
sudo date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z"
```
3. ✅ SUCCESS: RPi Clock gets set just fine!

### Raspberry Pi Boot Issues due to SD Card

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

## Links
- [Good article on Multiprocessing](https://analyticsindiamag.com/run-python-code-in-parallel-using-multiprocessing/#:~:text=Multiprocessing%20in%20Python%20enables%20the,run%20tasks%2Fprocesses%20in%20parallel.&text=Multiprocessing%20enables%20the%20computer%20to,involve%20a%20lot%20of%20computation.)  
- [Stack Overflow article on Multiprocessing with Lock](https://stackoverflow.com/questions/28267972/python-multiprocessing-locks)  
- [Article on 7-Segment-Display implementation](https://www.stuffaboutcode.com/2016/10/raspberry-pi-7-segment-display-gpiozero.html)  
- [Article on Keypad implementation](https://www.digikey.bg/en/maker/blogs/2021/how-to-connect-a-keypad-to-a-raspberry-pi)  
- [Article on Stepping Motor](https://www.aranacorp.com/en/control-a-stepper-with-raspberrypi/)  
