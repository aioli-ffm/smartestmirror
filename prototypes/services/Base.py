#!/usr/bin/python
'''
author: Christian M
'''
from abc import abstractmethod
from Configurateable import *

class Base(Configurateable):

    def __init__(self):
        super(Base, self).__init__()
        self.serviceRunner = None

    @classmethod
    @abstractmethod
    def init(self):
        pass

    @classmethod
    @abstractmethod
    def update(self):
        pass
