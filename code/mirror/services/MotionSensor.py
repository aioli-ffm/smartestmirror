#!/usr/bin/python
'''
author: Christian M
'''
import serial
import time
import logging
from services.Base import *


class MotionSensor(Base):

    def __init__(self, serviceRunner):
        super(MotionSensor, self).__init__()
        self.serviceRunner = serviceRunner
        self.logger = logging.getLogger(__name__)

    def init(self):
        self.last_move = time.time()
        self.state = 1  # Mirror will be turned on at start
        self.ser = serial.Serial()
        self.ser.baudrate = 9600
        self.ser.port = '/dev/arduino_motionsensor'
        try:
            self.ser.open()
            self.open = True
        except:
            self.logger.error("Serial port not usable")
            self.open = False
        self.callbacks = []

    def update(self):
        if self.open:
            self.checkMotion()

    def checkMotion(self):
        """
        read the serial motion sensor, turn on and off the TV and the widget-timers
        """
        res = 0
        while(self.ser.inWaiting() > 0):
            res = self.ser.readline().strip()

        try:
            if self.state == 1 and time.time() - self.last_move > self.config["keep_on_time"]:
                self.execOff()

            if res == "1":
                self.last_move = time.time()

            if res == "1" and self.state == 0:
                self.execOn()
        except Exception as e:
            self.logger.error(e)

    def execOn(self):
        self.logger.info("Motionsensing: Turning TV on")
        self.state = 1
        for callback in self.callbacks:
            callback(self.state)

    def execOff(self):
        self.logger.info("Motionsensing: Turning TV off")
        self.state = 0
        for callback in self.callbacks:
            callback(self.state)

    def addCallback(self, callback):
        self.callbacks.append(callback)
