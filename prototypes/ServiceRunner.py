#!/usr/bin/python
'''
author: Christian M
'''
import importlib
import pkgutil
import services


class ServiceRunner(object):

    def init(self):
        self.loadServices()

    def run(self):
        pass

    def loadServices(self):
        self.services = []
        self.timers = []
        for importer,modname,ispkg in pkgutil.iter_modules(services.__path__):
            if modname != "Base":
                print("Found service %s" % modname)
                mod = importlib.import_module("services."+modname)
                class_ = getattr(mod, modname)
                instance = class_(self)
                instance.init()
                self.services.append(instance)
