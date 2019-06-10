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
import logging

class Mirror(QLabel,Base):
    """
    Get webcam images, process and display them
    """
    def __init__(self, title, parent, serviceRunner):
        super(Mirror,self).__init__(title,parent)
        self.logger = logging.getLogger(__name__)
        self.serviceRunner = serviceRunner
        self.parent = parent
        self.downloadHaarcascade()
        self.detectFace = True
        if self.detectFace:
            self.face_cascade = cv2.CascadeClassifier('./supplementary/haarcascade_frontalface_default.xml')

    def downloadHaarcascade(self):
        import urllib
        if not os.path.isfile("./supplementary/haarcascade_frontalface_default.xml"): 
            self.logger.info("Downloading Haarcascade")
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

            for (x,y,w,h) in faces:
                cv2.rectangle(mirror_color, (x,y),(x+w,y+h),(255,0,255),4)

            # scale for width
            new_height = int(img.shape[0] / (img.shape[1]/float(self.config["width"])))
            # resize for display
            mirror_color = cv2.resize(mirror_color, (self.config["width"], new_height)) 
            self.setimg(mirror_color) # show img if no face is found

        else:
            self.logger.warn("Image is None")
