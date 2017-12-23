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

    def defaultConfig(self):
        return {"x":0, "y":0, "Interval":1, "resx":640, "resy":480}

    def init(self):
        self.capture = cv2.VideoCapture(0)
        self.image = self.capture.read()

    def update(self):
        ret,self.image = self.capture.read()

    def currentImage(self):
        return self.image
