#!/usr/bin/python
'''
author: Christian M
'''

import time
import logging
import cec
from services.Base import *


class TV(Base):

    def __init__(self, serviceRunner):
        super(TV, self).__init__()
        self.serviceRunner = serviceRunner
        self.logger = logging.getLogger(__name__)

    def defaultConfig(self):
        return {}

    def init(self):
        try:
            cec.init()  # AttributeError: 'module' object has no attribute 'init'
            self.tv = cec.Device(cec.CECDEVICE_TV)
            self.serviceRunner.services["MotionSensor"].addCallback(self.callback)
            self.callback(True)
        except Exception as e:
            self.logger.error("==================================")
            self.logger.error("Cannot take control of TV: ", e)
            self.logger.error("==================================")

    def update(self):
        pass

    def callback(self, isOn):
        if isOn:
            self.logger.info("Power_on")
            self.tv.power_on()
        else:
            self.logger.info("Standby")
            self.tv.standby()
