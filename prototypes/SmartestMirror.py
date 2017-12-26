#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
author: Christian M
'''
import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import ServiceRunner
import WidgetRunner
import ProfileManager

class SmartestMirror(QWidget):
    def __init__(self):
        super(SmartestMirror,self).__init__()
        self.initUI()
        
        self.serviceRunner = ServiceRunner.ServiceRunner()
        self.serviceRunner.init()
        self.widgetRunner = WidgetRunner.WidgetRunner(self, self.serviceRunner)
        self.widgetRunner.init()
        self.profileManager = ProfileManager.ProfileManager(self.serviceRunner, self.widgetRunner)

    def initUI(self):
        self.setAcceptDrops(True)
        # create window, geometry and colors
        self.setWindowTitle('Smartestmirror')
        self.setGeometry(0, 0, 1080, 1920)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        position = e.pos()
        self.current_drag.move(position)
        e.setDropAction(Qt.MoveAction)
        e.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SmartestMirror()
    ex.show()
    app.exec_()
