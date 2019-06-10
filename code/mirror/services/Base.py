#!/usr/bin/python
'''
author: Christian M
'''
from abc import abstractmethod
import logging

class Base(object):

    def __init__(self):
        super(Base, self).__init__()
        self.serviceRunner = None
        self.config = {}

    @classmethod
    @abstractmethod
    def defaultConfig(self):
        return{"Interval":1}

    @classmethod
    @abstractmethod
    def init(self):
        pass

    @classmethod
    @abstractmethod
    def update(self):
        pass
