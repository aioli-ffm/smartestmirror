#!/usr/bin/python
'''
author: Christian M
'''
import time
import cec
from services.Base import *

class TV(Base):

    def __init__(self):
        self.init()

    def init(self):
        cec.init()
        self.tv = cec.Device(cec.CECDEVICE_TV)
        # MotionSensor.addCallback(self.callback)

    def run(self):
        pass

    def callback(self, isOn):
        if isOn:
            self.tv.power_on()
        else:
            self.tv.power_off()
