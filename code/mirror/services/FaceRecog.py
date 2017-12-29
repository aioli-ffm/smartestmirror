#!/usr/bin/python
'''
author: Christian M
'''
import cv2
from services.Base import *
from supplementary.Predictor import *

class FaceRecog(Base):
    def __init__(self, serviceRunner):
        super(FaceRecog, self).__init__()
        self.serviceRunner = serviceRunner
        self.predictor = Predictor()

    def defaultConfig(self):
        return {"Interval":0.5}

    def update(self):
        # try to find and recognize face(s)
        self.predictor.setImage(self.serviceRunner.services["Webcam"].currentImage())
        self.predictor.extractFace(save=True)
        predictions = self.predictor.pred()
