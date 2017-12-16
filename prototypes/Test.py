import unittest
from services import Webcam, MotionSensor
from widgets import Bitcoin
import Config
import ServiceRunner, WidgetRunner

import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *

class TestConfigMethods(unittest.TestCase):

    def test_tojson(self):
        webcam = Webcam.Webcam(None)
        config = Config.Config()
        webcam.config = webcam.defaultConfig()
        print(config.toJSON(webcam))

    def test_save(self):
        webcam = Webcam.Webcam(None)
        motion = MotionSensor.MotionSensor(None)
        config = Config.Config()
        configurateables = []
        configurateables.append(webcam)
        configurateables.append(motion)
        webcam.config = webcam.defaultConfig()
        config.save(configurateables, "test.json")

    def test_load(self):
        webcam = Webcam.Webcam(None)
        motion = MotionSensor.MotionSensor(None)
        config = Config.Config()
        configurateables = []
        configurateables.append(webcam)
        configurateables.append(motion)
        config.load(configurateables, "test.json")
        print(webcam.config)

class TestWidgets(unittest.TestCase):

    def test_bitcoin(self):
        app = QApplication(sys.argv)
        serviceRunner = ServiceRunner.ServiceRunner()
        serviceRunner.init()
        print(serviceRunner.services)
        widgetRunner = WidgetRunner.WidgetRunner(parent=None, serviceRunner=serviceRunner)
        widgetRunner.init()
        bitcoin = widgetRunner.widgets["Bitcoin"]
        print(bitcoin.config["Currency"])
    def test_widgetsrunner(self):
        pass

if __name__ == '__main__':
    unittest.main()