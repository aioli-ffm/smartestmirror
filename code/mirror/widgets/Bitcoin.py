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

class Bitcoin(QLabel, Base):
    """
    Display Bitcoin
    """
    def __init__(self, title, parent, serviceRunner):
        super(Bitcoin, self).__init__(title, parent)
        self.parent = parent
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("color: rgb(255,255,255);")

    def defaultConfig(self):
        return {"x":50, "y":900, "Interval":600, "Currency":"EUR"}

    def settext(self,text):
        self.setText(text)

        f = self.font()
        m = QFontMetrics(f)
        size = m.size(0, self.text())
        self.setFixedSize(size.width(), size.height())

    def update(self):
        try:
            r = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')

            updated = r.json()['time']['updated']
            price = r.json()['bpi'][self.config["Currency"]]['rate_float']

            dstr = "%.2f EUR (%s)" % (price, updated)
            self.settext(dstr)
        except Exception, e:
            pass
