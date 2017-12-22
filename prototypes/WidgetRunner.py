#!/usr/bin/python
'''
author: Christian M
'''
import widgets
import Config

from PyQt5.QtCore import *

import importlib
import pkgutil

class WidgetRunner(object):

    def __init__(self, parent, serviceRunner):
        self.serviceRunner = serviceRunner
        self.parent = parent
        self.config = Config.Config()
        self.widgets = {}
        self.timers = []

    def init(self):
        self.loadWidgets()
        self.configWidgets()
        self.initWidgets()
        self.startWidgets()

    def loadWidgets(self):
        for importer,modname,ispkg in pkgutil.iter_modules(widgets.__path__):
            if modname != "Base":
                print("Found widget %s" % modname)
                mod = importlib.import_module("widgets."+modname)
                class_ = getattr(mod, modname)
                instance = class_(title=modname, parent=self.parent, serviceRunner=self.serviceRunner)
                self.widgets[modname] = instance    

    def configWidgets(self,profile="Default.json"):
        self.config.load(self.widgets.values(), profile)

    def initWidgets(self,profile="Default.json"):
        for widget in self.widgets.values():
            if not self.config.isEnabled(widget,profile):
                widget.hide()
                continue
            widget.init()
            try:
                widget.move(widget.config["x"], widget.config["y"])
            except Exception as e:
                widget.hide()
                print("No position info for module %s"%widget)
                print("Exception: ", e)

    def startWidgets(self,profile="Default.json"):
        for widget in self.widgets.values():
            if not self.config.isEnabled(widget,profile):
                continue
            # setup the update functions
            timer = QTimer()
            timer.timeout.connect(widget.update)
            timer.start(widget.config['Interval']*1000) # from s to Ms for the timer
            widget.update()
            self.timers.append(timer)

    def stopWidgets(self):
        for timer in self.timers:
            timer.stop()
