#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import configparser
import sys
import datetime

import widgets
#from widgets import *
#from widgets.TimerText import TimerText

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

        self.initUI()
        self.current_drag = None

        
    def initUI(self):
        self.setAcceptDrops(True)

        # create window, geometry and colors
        self.setWindowTitle('Smartestmirror')
        self.setGeometry(0, 0, self.config.getint("Display","w"), self.config.getint("Display","h"))
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        self.getWidgets()


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
                    timer.start(int(self.config[modname]['Interval']))
                    self.timers.append(timer)
                    for opt in self.config.options(modname):
                        print("\t%s:%s"%(opt, self.config[modname][opt]))

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
