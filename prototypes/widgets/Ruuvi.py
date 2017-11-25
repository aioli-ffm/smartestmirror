#!/usr/bin/python
'''
author: Christian M
'''

from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import datetime
import calendar
from widgets.Base import *
from ruuvitag_sensor.ruuvi import RuuviTagSensor

class Ruuvi(QLabel,Base):
    """
    Display ruuvi tag, temperature and humidity
    """
    def __init__(self, title, parent):
        super(Ruuvi,self).__init__(title,parent)
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
        try:
            datas = RuuviTagSensor.get_data_for_sensors()
            humidity = datas[list(datas)[0]]['humidity']
            temperature = datas[list(datas)[0]]['temperature']
            pressure = datas[list(datas)[0]]['pressure']
            self.settext("humidity: " + str(humidity) + " %\n" + "temperature: " + str(temperature) + " °C\n" + "pressure: " + str(pressure) + " hPa")
        except:
            pass
