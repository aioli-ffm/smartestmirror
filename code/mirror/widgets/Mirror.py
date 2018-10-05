#!/usr/bin/python
'''
author: Tobias Weis, Christian M
'''
import cv2
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import datetime
import calendar
import numpy as np
from widgets.Base import *
import time
import os

class Mirror(QLabel,Base):
    """
    Get webcam images, process and display them
    """
    def __init__(self, title, parent, serviceRunner):
        super(Mirror,self).__init__(title,parent)
        self.serviceRunner = serviceRunner
        self.parent = parent
        self.downloadHaarcascade()
        self.detectFace = True
        self.zoomFace = True
        if self.detectFace:
            self.face_cascade = cv2.CascadeClassifier('./supplementary/haarcascade_frontalface_default.xml')
        self.serviceRunner.get("SpeechCommands").addCallback("on", self.command_callback)

    def command_callback(self, _):
        self.zoomFace = not self.zoomFace

    def downloadHaarcascade(self):
        import urllib
        if not os.path.isfile("./supplementary/haarcascade_frontalface_default.xml"): 
            print("Downloading Haarcascade")
            testfile = urllib.URLopener()
            testfile.retrieve("https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml", "./supplementary/haarcascade_frontalface_default.xml")

    def setimg(self,img):
        img = np.require(img, np.uint8, 'C')
        qimg = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.setPixmap(pixmap)

    def update(self):
        img = self.serviceRunner.get("Webcam").currentImage()
        if img is not None:
            mirror_color = cv2.flip(img,1)
            gray = cv2.cvtColor(mirror_color, cv2.COLOR_BGR2GRAY)

            faces = []
            if self.detectFace:
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) == 0:
                self.setimg(mirror_color) # show img if no face is found

            if self.zoomFace and self.detectFace:
                for (x,y,w,h) in faces:
                    roi_color = mirror_color[y:y+h, x:x+w]
                    height, width = mirror_color.shape[:2]
                    zoomed_color = cv2.resize(roi_color,(height, height), interpolation = cv2.INTER_CUBIC)
                    self.setimg(zoomed_color)
        else:
            print("None")
