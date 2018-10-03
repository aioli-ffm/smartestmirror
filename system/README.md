udev-rules, system-scripts etc. go here

## startup-scripts (on X-Server/ubuntu start)
To automatically setup the screen-orientation, disable blanking and start the mirror,
put the file startup_smartestmirror.desktop in the folder ~/.config/autostart/

## udev-rules
*udev-rule for motionsensing: 
```
SUBSYSTEMS=="usb", ATTRS{idProduct}=="7523", ATTRS{idVendor}=="1a86", SYMLINK+="arduino_motionsensor"
```
