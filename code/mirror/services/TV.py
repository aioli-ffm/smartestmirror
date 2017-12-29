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

    def defaultConfig(self):
        return {}

    def init(self):
        try:
            cec.init()  # AttributeError: 'module' object has no attribute 'init'
            self.tv = cec.Device(cec.CECDEVICE_TV)
            self.serviceRunner.services["MotionSensor"].addCallback(
                self.callback)
            self.callback(True)
        except Exception as e:
            print("==================================")
            print("Cannot take control of TV: ", e)
            print("==================================")

    def update(self):
        pass

    def callback(self, isOn):
        if isOn:
            print("----------------TV: power_on")
            self.tv.power_on()
        else:
            print("----------------TV: standby")
            self.tv.standby()
