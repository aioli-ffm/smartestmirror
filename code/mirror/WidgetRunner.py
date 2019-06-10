#!/usr/bin/python
'''
author: Christian M
'''
import widgets
import Config

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QGridLayout, QLayout

import importlib
import pkgutil

class WidgetRunner(object):

    def __init__(self, parent, serviceRunner):
        self.serviceRunner = serviceRunner
        self.parent = parent
        self.config = Config.Config()
        #self.grid = QGridLayout()
        #self.parent.setLayout(self.grid)


    def init(self, profile="./profiles/Default.json"):

        self.serviceRunner.services["MotionSensor"].addCallback(self.callback)
        self.widgets = {}
        self.timers = []

        self.profile = profile
        self.loadWidgets()
        self.configWidgets()
        self.initWidgets()
        self.startWidgets()

    def clear(self):
        for w,v in self.widgets.iteritems():
            #v.setParent(None)
            v.deleteLater()

        del self.widgets
        del self.timers

        self.widgets = {}
        self.timers = []

    def loadWidgets(self):
        for importer,modname,ispkg in pkgutil.iter_modules(widgets.__path__):
            if modname != "Base":
                print("Found widget %s" % modname)
                try:
                    mod = importlib.import_module("widgets."+modname)
                    class_ = getattr(mod, modname)
                    instance = class_(title=modname, parent=self.parent, serviceRunner=self.serviceRunner)
                    self.widgets[modname] = instance
                except Exception as e:
                    print('module exception in '+ modname,e) 
                #self.grid.addWidget(instance)
                #self.parent.addWidget(instance)

    def configWidgets(self):
        self.config.load(self.widgets.values(), self.profile)

    def initWidgets(self):
        for widget in self.widgets.values():
            if not self.config.isEnabled(widget,self.profile):
                widget.hide()
                continue
            widget.init()
            try:
                widget.move(
                        int(widget.config["x"]), 
                        int(widget.config["y"])
                        )
            except Exception as e:
                widget.hide()
                print("No position info for module %s"%widget)
                print("[WidgetRunner] Exception: ", e)

    def callback(self, isOn):
        if isOn:
            self.startWidgets()
            print("[WidgetRunner] Start Widgets")
        else:
            self.stopWidgets()
            print("[WidgetRunner] Stop Widgets")

    def startWidgets(self):
        for widget in self.widgets.values():
            if not self.config.isEnabled(widget,self.profile):
                print("Widget not enabled: ", widget)
                continue
            # setup the update functions
            timer = QTimer()
            timer.timeout.connect(widget.update)
            timer.start(float(widget.config['Interval'])*1000) # from s to Ms for the timer
            widget.update()
            widget.show()
            self.timers.append(timer)

    def stopWidgets(self):
        for timer in self.timers:
            timer.stop()
