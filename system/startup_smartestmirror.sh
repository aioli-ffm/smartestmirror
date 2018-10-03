#!/bin/bash
export DISPLAY=:0

# rotate display
xrandr --output HDMI-0 --rotate right

# disable blanking
xset s off
xset -dpms
xset s noblank

# start smartmirror-script
screen -dm bash -c "export DISPLAY=:0; cd /home/nvidia/code/smartestmirror/code/mirror/; ./SmartestMirror.py;exec sh"

echo "Started."
