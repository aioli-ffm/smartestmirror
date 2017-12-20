#!/usr/bin/python
'''
author: Christian M
'''
import os
from services.Base import *

class TTS(Base):

    def __init__(self, serviceRunner):
        super(TTS, self).__init__()
        self.serviceRunner = serviceRunner
        self.config = self.defaultConfig()

    def defaultConfig(self):
        return {"voice":"en", "speed":1}

    def init(self):
        self.say("Starting")

    def say(self, text):
        os.system("espeak '"+text+"'")
