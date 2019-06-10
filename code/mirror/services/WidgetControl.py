#!/usr/bin/python
'''
author: Tobias W.
'''
import cv2
from services.Base import *
import WidgetRunner
import logging

class WidgetControl(Base):
    def __init__(self, serviceRunner):
        super(WidgetControl, self).__init__()
        self.serviceRunner = serviceRunner
        self.logger = logging.getLogger(__name__)

    def defaultConfig(self):
        return {"x":0, "y":0, "Interval":1, "resx":640, "resy":480}

    def init(self):
        self.cnt = 0

    def update(self):
        if self.cnt > 1:
            self.logger.info(self.cnt)
            if self.cnt % 2 == 0:
                self.serviceRunner.parent.profileManager.load("Tobi")
            else:
                self.serviceRunner.parent.profileManager.load("Default")
        self.cnt += 1
