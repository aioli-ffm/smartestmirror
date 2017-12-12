#!/usr/bin/python
'''
author: Christian M
'''

class ServiceRunner(object):

    def init(self):
        pass

    def run(self):
        pass

    def loadServices(self):
        self.widgets = []
        self.timers = []

        import importlib
        import pkgutil

        for importer,modname,ispkg in pkgutil.iter_modules('.'):
            if modname != "Base":
                print("Found service %s" % modname)
