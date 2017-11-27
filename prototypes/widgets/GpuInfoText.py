#!/usr/bin/python
'''
author: Tobias Weis, Christian M
'''
import commands
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from widgets.Base import *

class GpuInfoText(QLabel,Base):
    """
    Display GPU Temperature
    """
    def __init__(self, title, parent):
        super(GpuInfoText,self).__init__(title,parent)
        self.parent = parent
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("color: rgb(255,255,255);")


    def settext(self,text):
        self.setText(text)
        newfont = QFont("Times", 22, QFont.Bold) 
        self.setFont(newfont)

        f = self.font()
        m = QFontMetrics(f)
        size = m.size(0, self.text())
        self.setFixedSize(size.width(), size.height())

    def update(self):
        self.settext(commands.getoutput("nvidia-smi -q -d TEMPERATURE | grep Current"))
