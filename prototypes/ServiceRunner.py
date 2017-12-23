#!/usr/bin/python
'''
author: Christian M
'''
import services
import Config

from PyQt5.QtCore import *

import importlib
import pkgutil

class ServiceRunner(object):

    def __init__(self):
        self.config = Config.Config()
        self.services = {}
        self.timers = []

    def init(self):
        self.loadServices()
        self.configServices()
        self.initServices()
        self.startServices()

    def loadServices(self):
        for importer,modname,ispkg in pkgutil.iter_modules(services.__path__):
            if modname != "Base":
                print("Found service %s" % modname)
                mod = importlib.import_module("services."+modname)
                class_ = getattr(mod, modname)
                instance = class_(self)
                self.services[modname] = instance

    def configServices(self, profile="Default.json"):
        self.config.load(self.services.values(), profile)

    def initServices(self, profile="Default.json"):
        for service in self.services.values():
            if not self.config.isEnabled(service,profile):
                continue
            service.init()

    def startServices(self, profile="Default.json"):
        for service in self.services.values():
            if not self.config.isEnabled(service,profile):
                continue
            # setup the update functions
            timer = QTimer()
            timer.timeout.connect(service.update)
            timer.start(service.config['Interval']*1000) # from s to Ms for the timer
            service.update()
            self.timers.append(timer)

    def stopServices(self):
        for timer in self.timers:
            timer.stop()

    def get(self, name):
        return self.services[name]
