#!/usr/bin/python
'''
author: Tobias Weis, Christian M
'''
import os
import commands
import psutil
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from widgets.Base import *

class InfoText(QLabel,Base):
    """
    Display GPU Temperature
    """
    def __init__(self, title, parent, serviceRunner):
        super(InfoText,self).__init__(title,parent)
        self.parent = parent
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("color: rgb(255,255,255);")

    def settext(self,text):
        self.setText(text)
        newfont = QFont("Times", 16, QFont.Bold) 
        self.setFont(newfont)

        f = self.font()
        m = QFontMetrics(f)
        size = m.size(0, self.text())
        self.setFixedSize(size.width(), size.height())

    def update(self):
        loadavg = os.getloadavg()
        text = ""
        text = "Load: %.2f, %.2f, %.2f" % (loadavg[0], loadavg[1], loadavg[2]) # load over 1,5,15 minutes
        text += "\n"
	# if not on tegra
	try:
		temps = psutil.sensors_temperatures()
		text += "Temp: %.2f C" % (temps["coretemp"][0][1])
		text += "\n"
	except:
		pass

	# if on tegra
	try:
		temps = psutil.sensors_temperatures()
		text += "CPU: %.2f C, GPU: %.2f C" % (temps['MCPU-therm'][0][1], temps['GPU-therm'][0][1])
		text += "\n"
	except:
		pass

	# if not on tegra and with GPU
	try:
	    nvidiatext += commands.getoutput("nvidia-smi -q -d TEMPERATURE | grep Current")
	    if not "not found" in nvidiatext:
		text += nvidiatext
		text += "\n"
	except:
	    pass
        self.settext(text)
