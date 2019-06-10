#!/usr/bin/python
'''
author: Christian M
'''
import cv2
import numpy as np
from services.Base import *

class Webcam(Base):

    def __init__(self, serviceRunner):
        super(Webcam, self).__init__()
        self.serviceRunner = serviceRunner
        self.config = self.defaultConfig()
        self.image = None

    def defaultConfig(self):
        return {"x": 0, "y": 0, "Interval": 1, "resx": 640, "resy": 480, "device": 0}

    def init(self):
        self.capture = cv2.VideoCapture(self.config['device'])
        if not self.capture.isOpened():
            print("Could not open camera ", self.config['device'])
            img = np.zeros((self.config["resy"], self.config["resx"], 3), np.uint8)
            img += np.array([0,255,0], np.uint8)
            cv2.putText(img, 'No image, device %d'%(self.config["device"]), (10,self.config["resy"]/2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),1)
            self.image = img[:,::-1,:] #will be displayed mirrored
        else:
            self.capture.set(3,self.config["resx"])
            self.capture.set(4,self.config["resy"])

            ret, self.image = self.capture.read()

    def update(self):
        if self.capture.isOpened():
            ret, self.image = self.capture.read()
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

    def currentImage(self):
        return self.image
