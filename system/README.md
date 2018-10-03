udev-rules, system-scripts etc. go here

## udev-rules
*udev-rule for motionsensing: 
```
SUBSYSTEMS=="usb", ATTRS{idProduct}=="7523", ATTRS{idVendor}=="1a86", SYMLINK+="arduino_motionsensor"
```
