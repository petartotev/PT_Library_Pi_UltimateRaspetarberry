#! /bin/sh
cp /home/user/Desktop/raspberry-pi-logo.jpg /home/user/Desktop/`date +%Y-%m-%d`.jpg
sudo chmod ugo+rwx /home/user/Desktop/`date +%Y-%m-%d`.jpg
python3.9 /home/user/Desktop/project_pi4_nasa_api_wallpaper_python.py
export DISPLAY=:0
export XAUTHORITY=/home/user/.Xauthority
export XDG_RUNTIME_DIR=/run/user/1000
pcmanfm --set-wallpaper /home/user/Desktop/`date +%Y-%m-%d`.jpg
