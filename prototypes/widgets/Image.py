#!/usr/bin/python
'''
author: Tobias Weis
'''

from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image, ImageQt
import datetime
import calendar
import cv2
import numpy as np
from widgets.Base import *

class Image(QLabel,Base):
    """
    Display time and date
    """
    def __init__(self, title, parent):
        super(Image,self).__init__(title,parent)
        self.parent = parent
        #self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.setAlignment(Qt.AlignCenter)
        #self.setStyleSheet("color: rgb(255,255,255);")

    def setimg(self,img):
        img = np.require(img, np.uint8, 'C')
        qimg = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.setPixmap(pixmap)

    def update(self):
        # create a pretty timestring
        #img = np.zeros((100,200,3), np.uint8) + [255,255,255]
        img = cv2.imread("brain.jpg")
        self.setimg(img)
