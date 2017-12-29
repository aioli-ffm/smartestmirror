#!/usr/bin/python
'''
author: Christian M
'''
import serial
import time
from services.Base import *

class MotionSensor(Base):

    def __init__(self, serviceRunner):
        super(MotionSensor, self).__init__()
        self.serviceRunner = serviceRunner

    def init(self):
        self.last_move = 0
        self.state = 0
        self.ser = serial.Serial()
        self.ser.baudrate = 9600
        self.ser.port = '/dev/arduino_motionsensor'
        try:
            self.ser.open()
            self.open = True
        except:
            print("Serial port not usable")
            self.open = False
        self.callbacks = []

    def update(self):
        if self.open:
            self.checkMotion()

    def checkMotion(self):
        """
        read the serial motion sensor, turn on and off the TV and the widget-timers
        """
        res = self.ser.readline()
        try:
            if self.state == 1 and time.time() - self.last_move > 2 * 60:  # FIXME: hardcoded keep-on-time
                self.execOff()
                
            if not "0" in res:
                self.last_move = time.time()

            if "0" not in res and self.state == 0:
                self.execOn()
        except Exception as e:
            print("Exception: ", e)

    def execOn(self):
        self.state = 1
        for callback in self.callbacks:
            callback(self.state)

    def execOff(self):
        self.state = 0
        for callback in self.callbacks:
            callback(self.state)

    def addCallback(self, callback):
        self.callbacks.append(callback)
