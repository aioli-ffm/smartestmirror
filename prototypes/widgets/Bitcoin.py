#!/usr/bin/python
'''
author: Tobias Weis
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

class Bitcoin(QLabel,Base):
    """
    Display time and date
    """
    def __init__(self, title, parent):
        super(Bitcoin, self).__init__(title,parent)
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
        r = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')

        updated = r.json()['time']['updated']
        price = r.json()['bpi']['EUR']['rate_float']

        dstr = "%.2f EUR (%s)" % (price, updated)
        self.settext(dstr)
