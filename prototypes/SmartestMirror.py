#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
author: Christian M
'''
import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from services import ServiceRunner

class SmartestMirror(QWidget):
    def __init__(self):
        super(SmartestMirror,self).__init__()
        self.serviceRunner = ServiceRunner.ServiceRunner()
        self.serviceRunner.init()
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        # create window, geometry and colors
        self.setWindowTitle('Smartestmirror')
        #self.setGeometry(0, 0, self.config.getint("Display","w"), self.config.getint("Display","h"))
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SmartestMirror()
    ex.show()
    app.exec_()