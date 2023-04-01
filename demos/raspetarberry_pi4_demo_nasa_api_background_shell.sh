#! /bin/sh
cp /home/user/Desktop/raspberry-pi-logo.jpg /home/user/Desktop/`date +%Y-%m-%d`.jpg
sudo chmod ugo+rwx /home/user/Desktop/`date +%Y-%m-%d`.jpg
python3.9 /home/user/Desktop/raspetarberry_pi4_demo_nasa_api_change_background_python.sh
export DISPLAY=:0
export XAUTHORITY=/home/user/.Xauthority
export XDG_RUNTIME_DIR=/run/user/1000
pcmanfm --set-wallpaper /home/user/Desktop/`date +%Y-%m-%d`.jpg
