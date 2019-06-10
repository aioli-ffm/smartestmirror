#!/usr/bin/python
'''
author: Christian M
'''
import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QGridLayout, QLayout

import importlib
import pkgutil
import logging

import widgets
import Config

class WidgetRunner(object):

    def __init__(self, parent, serviceRunner):
        self.serviceRunner = serviceRunner
        self.parent = parent
        self.config = Config.Config()
        self.logger = logging.getLogger(__name__)

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
                self.logger.debug("Found widget %s" % modname)
                try:
                    mod = importlib.import_module("widgets."+modname)
                    class_ = getattr(mod, modname)
                    instance = class_(title=modname, parent=self.parent, serviceRunner=self.serviceRunner)
                    self.widgets[modname] = instance
                except Exception as e:
                    self.logger.error('module exception in '+ modname) 
                    self.logger.error(e)

    def configWidgets(self):
        self.config.load(self.widgets.values(), self.profile)

    def initWidgets(self):
        for widget in self.widgets.values():
            if not self.config.isEnabled(widget,self.profile):
                widget.hide()
                continue
            widget.init()
            widget.res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')

            try:
                widget.move(
                        int(widget.config["x"]), 
                        int(widget.config["y"])
                        )
            except Exception as e:
                widget.hide()
                self.logger.warn("No position info for module %s"%widget)
                self.logger.warn(e)

    def callback(self, isOn):
        if isOn:
            self.startWidgets()
            self.logger.info("Start Widgets")
        else:
            self.stopWidgets()
            self.logger.info("Stop Widgets")

    def startWidgets(self):
        for widget in self.widgets.values():
            if not self.config.isEnabled(widget,self.profile):
                self.logger.debug("Widget not enabled: %s" % widget)
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
