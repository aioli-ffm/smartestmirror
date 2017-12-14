#!/usr/bin/python
'''
author: Christian M
'''

class ServiceRunner(object):

    def init(self):
        self.loadServices()

    def run(self):
        pass

    def loadServices(self):
        self.services = []
        self.timers = []

        import importlib
        import pkgutil

        for importer,modname,ispkg in pkgutil.iter_modules('services'):
            if modname != "Base":
                print("Found service %s" % modname)
                mod = importlib.import_module("services."+modname)
                class_ = getattr(mod, modname)
                instance = class_(self)
                instance.init()
                self.services.append(instance)
