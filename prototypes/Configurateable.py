#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
author: Christian M
'''
from abc import abstractmethod
class Configurateable(object):

    def __init__(self):
        self.config = {}

    @classmethod
    @abstractmethod
    def defaultConfig(self):
        return {"x":0, "y":0, "Interval":1}