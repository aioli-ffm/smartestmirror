#!/usr/bin/python
'''
author: Christian M
'''
import cv2
from services.Base import *


class Webcam(Base):

    def __init__(self, serviceRunner):
        super(Webcam, self).__init__()
        self.serviceRunner = serviceRunner
        self.config = self.defaultConfig()

    def defaultConfig(self):
        return {"x": 0, "y": 0, "Interval": 1, "resx": 640, "resy": 480, "device": 0}

    def init(self):
        self.capture = cv2.VideoCapture(self.config['device'])
        if not self.capture.isOpened():
	        print("Could not open camera ", self.config['device'])
        ret, self.image = self.capture.read()

    def update(self):
        ret, self.image = self.capture.read()
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

    def currentImage(self):
        return self.image
