import unittest
from services import Webcam, MotionSensor
import Config

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

if __name__ == '__main__':
    unittest.main()