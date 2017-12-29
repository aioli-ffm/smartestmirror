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
        super(Display, self).__init__("", parent)
        self.parent = parent

    def init(self):
        self.parent.setGeometry(
            int(self.config["x"]),
            int(self.config["y"]),
            int(self.config["w"]),
            int(self.config["h"])
        )
        self.parent.setStyleSheet(self.config["style"])

    def defaultConfig(self):
        return {"x": 0, "y": 0, "w": 1080, "h": 1920, "style":"background-color:black;", "Interval": 10000}
