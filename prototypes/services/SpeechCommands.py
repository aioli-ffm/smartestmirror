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
        self.callbacks = {}
        self.config = self.defaultConfig()

    def defaultConfig(self):
        return {"graph":"conv_actions_frozen.pb", "labels":"conv_actions_labels.txt", "Interval": 100}

    def init(self):
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        #with self.m as source:
        #    self.r.adjust_for_ambient_noise(source)
        #self.stop_listening = self.r.listen_in_background(self.m, self.callback)

    def callback(self, recognizer, audio):
        try:
            spoken = recognizer.recognize_tensorflow(audio, tensor_graph=self.config.graph, tensor_label=self.config.labels)
            print(spoken)
        except sr.UnknownValueError:
            print("Tensorflow could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Tensorflow service; {0}".format(e))

    def addCallback(self, command, callback):
        callbacklist = []
        try:
            callbacklist = self.callbacks[command]
        except Exception:
            pass
        self.callbacks[command] = callbacklist
