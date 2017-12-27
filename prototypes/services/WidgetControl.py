#!/usr/bin/python
'''
author: Tobias W.
'''
import cv2
from services.Base import *
import WidgetRunner

class WidgetControl(Base):
    def __init__(self, serviceRunner):
        super(WidgetControl, self).__init__()
        self.serviceRunner = serviceRunner

    def defaultConfig(self):
        return {"x":0, "y":0, "Interval":1, "resx":640, "resy":480}

    def init(self):
        self.cnt = 0

    def update(self):
        if self.cnt > 1:
            print "------------ CNT: ", self.cnt
            if self.cnt % 2 == 0:
                print "Switching profile to Tobi"
                self.serviceRunner.widgetRunner.stopWidgets()
                self.serviceRunner.widgetRunner.clear()
                #self.serviceRunner.widgetRunner.parent.initUI()

                #self.serviceRunner.widgetRunner = WidgetRunner.WidgetRunner(self.serviceRunner.parent, self.serviceRunner)
                self.serviceRunner.widgetRunner.init(profile="Tobi.json")
                self.serviceRunner.parent.show()
            else:
                print "Switching profile to Default"
                self.serviceRunner.widgetRunner.stopWidgets()
                self.serviceRunner.widgetRunner.clear()
                #self.serviceRunner.widgetRunner.parent.initUI()
                
                #self.serviceRunner.widgetRunner = WidgetRunner.WidgetRunner(self.serviceRunner.parent, self.serviceRunner)
                self.serviceRunner.widgetRunner.init(profile="Default.json")
                self.serviceRunner.parent.show()
        self.cnt += 1
