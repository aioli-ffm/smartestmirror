#!/usr/bin/python
'''
author: Christian M
'''
import cv2
from services.Base import *

class Webcam(Base):

    def __init__(self):
        self.init()

    def init(self):
        self.capture = cv2.VideoCapture(0)
        self.image = None

    def run(self):
        ret,self.image = self.capture.read()

    def currentImage(self):
        return self.image
