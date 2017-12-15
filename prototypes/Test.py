import unittest
from services import Webcam
import Config

class TestConfigMethods(unittest.TestCase):

    def test_tojson(self):
        webcam = Webcam.Webcam(None)
        config = Config.Config()
        webcam.config = webcam.defaultConfig()
        print(config.toJSON(webcam))

if __name__ == '__main__':
    unittest.main()