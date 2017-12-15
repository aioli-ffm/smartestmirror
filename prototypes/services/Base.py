#!/usr/bin/python
'''
author: Christian M
'''
from abc import abstractmethod
from Configurateable import *

class Base(Configurateable):

    def __init__(self, serviceRunner):
        self.serviceRunner = serviceRunner

    @classmethod
    @abstractmethod
    def init(self):
        pass

    @classmethod
    @abstractmethod
    def run(self):
        pass
