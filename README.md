# smartestmirror
What's smarter than smart?

![Smartmirror 3D rendering](/doc/cropped-mirror_complete.png)

That's right! This fully configurable, extendable, AI/ML-boasting beast of a Smartmirror: The SmartestMirror!
Hardware-wise, it can run on any platform that is able to run linux, python and qt5.

![Smartmirror hardware rendering](/doc/mirror_portrait_split.png)

## Website
The official website to this project can be found here: http://www.smartestmirror.com

## Getting started
1. `git clone https://github.com/aioli-ffm/smartestmirror.git`
2. `cd smartestmirror/system && ./install_packages.sh`
3. optional, to make it startup at X-start: edit the paths in start_smartestmirror.desktop and startup_smartestmirror.sh and copy start_smartestmirror.desktop to ~/.config/autostart
4. To run the mirror-frontend manually: `cd smartestmirror/code/mirror/ && ./SmartestMirror.py`

## Configuration
The services, widgets and updaterates of these can be configured (for now) by editing the json-files in smartestmirror/code/mirror (Default.json for widgets, DefaultServices.json for Services). We are currently working on a web-based backend for an easier-to-use graphical configuration.

## User Profiles
A profile manager is able to switch user-profiles on-the-fly. So by attaching a button (lame) or detecting the identity of users using face-detection and -recognition, these profiles can be switched to display personalized information.

## Current research
We are currently working on fully unsupervised methods to learn the faces of the users of the mirror. The usecase we have in mind is the following: After being installed, all users should walk around in front of the mirror for some period of time, optimally covering a broad range of lighting-situations that will be encountered in production use. After that, our system will present the learned faces (which it is able to distinguish) in the backend, where users can name them and link them to personal profiles.
