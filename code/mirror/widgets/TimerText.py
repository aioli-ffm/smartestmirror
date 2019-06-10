#!/usr/bin/python
'''
author: Tobias Weis
'''

from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import datetime
import calendar
from widgets.Base import *

class TimerText(QLabel,Base):
    """
    Display time and date
    """
    def __init__(self, title, parent, serviceRunner):
        super(TimerText,self).__init__(title,parent)
        self.parent = parent
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("color: rgb(255,255,255);")

    def settext(self,text):
        self.setText(text)
        newfont = QFont("Helvetica", 22) 
        self.setFont(newfont)

        f = self.font()
        m = QFontMetrics(f)
        size = m.size(0, self.text())
        self.setFixedSize(size.width(), size.height())

    def update(self):
        # create a pretty timestring
        now = datetime.datetime.now()
        tstr = '%02d:%02d:%02d' % (now.hour, now.minute, now.second)
        # get the weekdays name
        wday = calendar.day_name[datetime.datetime.today().weekday()]
        # create a pretty datestring
        dstr = '%02d.%02d.%04d' % (now.day, now.month, now.year)
        #self.settext(tstr+"\n"+wday+", "+dstr)
        self.settext(tstr+" "+wday+", "+dstr)

