#!/usr/bin/python
'''
author: Christian M
'''
import widgets
import Config

class WidgetRunner(object):

    def __init__(self, parent, serviceRunner):
        self.serviceRunner = serviceRunner
        self.parent = parent
        self.config = Config.Config()

    def init(self):
        self.loadWidgets()
        self.configWidgets()
        self.initWidgets()

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
                self.widgets[modname] = instance

                

    def configWidgets(self):
        self.config.load(self.widgets.values(), "Default.json")

    def initWidgets(self):
        for widget in self.widgets.values():
            widget.init()
            try:
                widget.move(widget.config["x"], widget.config["y"])
            except Exception as e:
                print("No position info for module %s"%widget)
                print("Exception: ", e)