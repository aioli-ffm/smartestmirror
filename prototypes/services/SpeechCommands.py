#!/usr/bin/python
'''
author: Christian M
'''
import serial
import time
from services.Base import *
import speech_recognition as sr

class SpeechCommands(Base):

    def __init__(self, serviceRunner):
        super(SpeechCommands, self).__init__()
        self.serviceRunner = serviceRunner
        self.callbacks = []

    def init(self):
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        with self.m as source:
            self.r.adjust_for_ambient_noise(source)
        self.stop_listening = self.r.listen_in_background(self.m, self.callback)

    def callback(self, recognizer, audio):
        pass

    def addCallback(self, command, callback):
        self.callbacks.append(callback)
