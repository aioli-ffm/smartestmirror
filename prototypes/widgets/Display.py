#!/usr/bin/python
'''
author: Christian M
'''
from __future__ import print_function, unicode_literals 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from widgets.Base import *

class Display(QLabel, Base):
    """
    Display
    """
    def __init__(self, title, parent, serviceRunner):
        #super(Bitcoin, self).__init__(title, parent)
        self.parent = parent
        self.config = self.defaultConfig()

    def init(self):
        self.parent.setGeometry(self.config["x"], self.config["y"], self.config["w"], self.config["h"])

    def defaultConfig(self):
        return {"x":0, "y":0, "w":1920, "h":1080, "Interval":10000}

