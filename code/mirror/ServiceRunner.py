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

    def init(self, parent, widgetRunner):
        self.parent = parent
        self.widgetRunner = widgetRunner
        self.loadServices()
        self.configServices()
        self.initServices()
        self.startServices()

    def loadServices(self):
        for importer,modname,ispkg in pkgutil.iter_modules(services.__path__):
            if modname != "Base":
                print("Found service %s" % modname)
                try:
                    mod = importlib.import_module("services."+modname)
                    class_ = getattr(mod, modname)
                    instance = class_(self)
                    self.services[modname] = instance
                except Exception,e:
                    print('module exception in '+ modname,e)

    def configServices(self, profile="DefaultServices.json"):
        self.config.load(self.services.values(), profile)

    def initServices(self, profile="DefaultServices.json"):
        for service in self.services.values():
            if not self.config.isEnabled(service,profile):
                continue
            service.init()

    def startServices(self, profile="DefaultServices.json"):
        for service in self.services.values():
            if not self.config.isEnabled(service,profile):
                continue
            # setup the update functions
            timer = QTimer()
            timer.timeout.connect(service.update)
            timer.start(float(service.config['Interval'])*1000) # from s to Ms for the timer
            service.update()
            self.timers.append(timer)

    def stopServices(self):
        for timer in self.timers:
            timer.stop()

    def get(self, name):
        return self.services[name]
