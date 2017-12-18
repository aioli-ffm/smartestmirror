#!/usr/bin/python
'''
author: Christian M
'''
import time
import cec
from services.Base import *

class TV(Base):

    def __init__(self, serviceRunner):
        super(TV, self).__init__()
        self.serviceRunner = serviceRunner

    def init(self):
        #cec.init() # AttributeError: 'module' object has no attribute 'init'
        #self.tv = cec.Device(cec.CECDEVICE_TV)
        # MotionSensor.addCallback(self.callback)
        pass

    def update(self):
        pass

    def callback(self, isOn):
        if isOn:
            self.tv.power_on()
        else:
            self.tv.power_off()
