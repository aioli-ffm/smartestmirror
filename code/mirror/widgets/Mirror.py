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
        self.zoomFace = True
        if self.detectFace:
            self.face_cascade = cv2.CascadeClassifier('./supplementary/haarcascade_frontalface_default.xml')
        self.serviceRunner.get("SpeechCommands").addCallback("on", self.command_callback)

    def command_callback(self, _):
        self.zoomFace = not self.zoomFace

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

            if len(faces) == 0:
                # scale for width
                new_height = int(img.shape[0] / (img.shape[1]/float(self.config["width"])))
       	        # resize for display
                mirror_color = cv2.resize(mirror_color, (self.config["width"], new_height)) 
                self.setimg(mirror_color) # show img if no face is found

            if self.zoomFace and self.detectFace:
		new_img = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
                # calc width for single pics
                if len(faces) > 0:
			single_width = int(self.config["width"]/float(len(faces)))
                        idx = 0
			for (x,y,w,h) in faces:
			    roi_color = mirror_color[y:y+h, x:x+w]
			    height, width = mirror_color.shape[:2]

			    new_height = int(roi_color.shape[0] / (roi_color.shape[1]/float(single_width)))

                            # if its too large, rescale other dim also
                            if new_height > new_img.shape[0]:
                                new_width = int(roi_color.shape[1] / (roi_color.shape[0]/float(new_img.shape[0])))
			        zoomed_color = cv2.resize(roi_color,(new_width, new_img.shape[0]), interpolation = cv2.INTER_CUBIC)
                                new_img[:zoomed_color.shape[0],
                                        idx*single_width:idx*single_width+new_width,
                                        :] = zoomed_color
                            else:
			        zoomed_color = cv2.resize(roi_color,(single_width, new_height), interpolation = cv2.INTER_CUBIC)
                                new_img[:zoomed_color.shape[0],
                                        idx*single_width:(idx+1)*single_width,
                                        :] = zoomed_color

			    #zoomed_color = cv2.resize(roi_color,(height, height), interpolation = cv2.INTER_CUBIC)
                            idx += 1
		        self.setimg(new_img)
        else:
            self.logger.warn("Image is None")
