#!/usr/bin/python
'''
author: Tobias Weis, Christian M
'''
from __future__ import print_function, unicode_literals 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import datetime
import calendar
from widgets.Base import *
import json
import requests
import cv2
import numpy as np
import urllib

class Xkcd(QLabel, Base):
    """
    Display Xkcd comic
    """
    def __init__(self, title, parent, serviceRunner):
        super(Xkcd, self).__init__(title, parent)
        self.parent = parent
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("color: rgb(255,255,255);")

    def defaultConfig(self):
        return {"x":50, "y":900, "Interval":600}

    def setimg(self,img):
        img = np.require(img, np.uint8, 'C')
        qimg = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.setPixmap(pixmap)

    def update(self):
        r = requests.get('https://dynamic.xkcd.com/api-0/jsonp/comic')
        url = r.json()['img']
        resp = urllib.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        self.setimg(image)
