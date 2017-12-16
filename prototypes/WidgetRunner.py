#!/usr/bin/python
'''
author: Christian M
'''
import widgets

class WidgetRunner(object):

    def __init__(self, parent, serviceRunner):
        self.serviceRunner = serviceRunner
        self.parent = parent

    def init(self):
        self.loadWidgets()

    def run(self):
        pass

    def loadWidgets(self):
        self.widgets = {}
        self.timers = []

        import importlib
        import pkgutil

        for importer,modname,ispkg in pkgutil.iter_modules(widgets.__path__):
            if modname != "Base":
                print("Found widget %s" % modname)
                mod = importlib.import_module("widgets."+modname)
                class_ = getattr(mod, modname)
                instance = class_(title=modname, parent=self.parent, serviceRunner=self.serviceRunner)
                instance.init()
                self.widgets[modname] = instance
