#!/bin/bash
export DISPLAY=:0

# rotate display
xrandr --output HDMI-0 --rotate right

# disable blanking
xset s off
xset -dpms
xset s noblank

# set opencv env variable to allow correct webcam closing

# start smartmirror-script
screen -dm bash -c "export DISPLAY=:0; cd /home/nvidia/code/smartestmirror/code/mirror/;OPENCV_VIDEOIO_PRIORITY_MSMF=0 ./SmartestMirror.py;exec sh"


echo "Started."
