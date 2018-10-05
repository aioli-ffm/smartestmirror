#!/bin/bash
sudo apt-get install portaudio19-dev python-pip python-requests python-pyqt5 libcec-dev espeak python-yaml cmake

# build torch (only on TX2)
#git clone http://github.com/pytorch/pytorch
#cd pytorch
#git submodule update --init
#python setup.py build_deps
#sudo python setup.py install

# FIXME: global installs?
sudo pip install -r requirements.txt
