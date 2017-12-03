#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import ConfigParser
import sys
import datetime
import cec
import time
import serial

import widgets
#from widgets import *
#from widgets.TimerText import TimerText

class Canvas(QWidget):
    def __init__(self):
        super(Canvas,self).__init__()
        self.config = ConfigParser.ConfigParser()
        self.config.read("config.ini")

        self.initUI()
        self.current_drag = None

	self.ser = serial.Serial()
	self.ser.baudrate = 9600
	self.ser.port = '/dev/arduino_motionsensor'
	self.ser.open()

	cec.init()
	self.tv = cec.Device(cec.CECDEVICE_TV)

	self.last_move = 0
	self.state = 0

	# add timer to periodically check the motionsensor
	self.timer = QTimer()
	self.timer.timeout.connect(self.checkMotion)
	self.timer.start(5) # from s to Ms for the timer

        
    def initUI(self):
        self.setAcceptDrops(True)

        # create window, geometry and colors
        self.setWindowTitle('Smartestmirror')
        self.setGeometry(0, 0, self.config.getint("Display","w"), self.config.getint("Display","h"))
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        self.getWidgets()

    def checkMotion(self):
	"""
	read the serial motion sensor, turn on and off the TV and the widget-timers
	"""
	res = self.ser.readline()
	try:
		if self.state == 1 and time.time() - self.last_move > 10*60: # FIXME: hardcoded keep-on-time
		    print "Turning off"
		    self.tv.standby()
		    self.state = 0

		if not "0" in res:
		    self.last_move = time.time()

		if "0" not in res and self.state == 0:
		    self.state = 1
		    self.tv.power_on()
		    print "Turning on"
	except Exception as e:
		print "Exception: ", e


    def getWidgets(self):
        """ 
        parse available widgets,
        only add those that have a config section
        TODO: add some install routine for widgets that automatically create this config section!
        """
        self.widgets = []
        self.timers = []

        import importlib
        import pkgutil

        for importer,modname,ispkg in pkgutil.iter_modules(widgets.__path__):
            if modname != "Base":
                print("Found widget %s" % modname)
                # check if this module has a config-section
                if self.config.has_section(modname):
                    # import the module
                    mod = importlib.import_module("widgets."+modname)
                    # instantiate the widget
                    class_ = getattr(mod, modname)
                    instance = class_("TimerText",self)
                    instance.update()
                    # move to position
                    try:
                        instance.move(self.config.getint(modname,'x'),self.config.getint(modname,'y'))
                    except Exception as e:
                        print("No position info for module %s"%modname)
                        print("Exception: ", e)
                    self.widgets.append(instance)
                    # setup the update functions
                    timer = QTimer()
                    timer.timeout.connect(instance.update)
                    timer.start(self.config.getfloat(modname,'Interval')*1000) # from s to Ms for the timer
                    self.timers.append(timer)
                    for opt in self.config.options(modname):
                        print("\t%s:%s"%(opt, self.config.get(modname,opt)))

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        position = e.pos()
        self.current_drag.move(position)
        #self.button.move(position)

        e.setDropAction(Qt.MoveAction)
        e.accept()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Canvas()
    ex.show()
    app.exec_() 
