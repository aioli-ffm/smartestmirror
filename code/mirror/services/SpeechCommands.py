#!/usr/bin/python
'''
author: Christian M
'''
import serial
import time
import os
import zipfile
import logging
from services.Base import *
import speech_recognition as sr


class SpeechCommands(Base):

    modelfile = 'speech_commands_v0.01.zip'
    modelurl = 'http://download.tensorflow.org/models/speech_commands_v0.01.zip'
    callbacks = {}

    def __init__(self, serviceRunner):
        super(SpeechCommands, self).__init__()
        self.serviceRunner = serviceRunner
        self.callbacks = {}
        self.config = self.defaultConfig()
        self.downloadmodel()
        self.logger = logging.getLogger(__name__)

    def downloadmodel(self):
        import urllib
        if not os.path.isfile("./supplementary/" + self.modelfile):
            self.logger.info("Downloading Speech Commands model")
            testfile = urllib.URLopener()
            testfile.retrieve(
                self.modelurl, "./supplementary/" + self.modelfile)
            modelzip = zipfile.ZipFile(
                "./supplementary/" + self.modelfile, 'r')
            modelzip.extractall("./supplementary/")
            modelzip.close()

    def defaultConfig(self):
        return {"graph": "conv_actions_frozen.pb", "labels": "conv_actions_labels.txt", "Interval": 100}

    def init(self):
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        with self.m as source:
            self.r.adjust_for_ambient_noise(source)
        self.stop_listening = self.r.listen_in_background(
            self.m, self.callback)

    def callback(self, recognizer, audio):
        try:
            from tensorflow.contrib.framework.python.ops import audio_ops as contrib_audio
            graph = "./supplementary/" + str(self.config["graph"])
            labels = "./supplementary/" + str(self.config["labels"])
            spoken = recognizer.recognize_tensorflow(
                audio, tensor_graph=graph, tensor_label=labels)
            self.logger.debug(spoken)
        except sr.UnknownValueError:
            self.logger.debug("Tensorflow could not understand audio")
        except sr.RequestError as e:
            self.logger.error(
                "Could not request results from Tensorflow service; {0}".format(e))

    def executeCallbacks(self, command):
        try:
            callbacklist = self.callbacks[command]
            for callback in callbacklist:
                try:
                    callback(command)
                except Exception as e:
                    self.logger.error(e)
        except Exception as e:
            self.logger.error(e)

    def addCallback(self, command, callback):
        callbacklist = []
        try:
            callbacklist = self.callbacks[command]
        except Exception:
            pass
        callbacklist.append(callback)
        self.callbacks[command] = callbacklist
