#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
author: Christian M
'''
from abc import abstractmethod
class Configurateable(object):

    @classmethod
    @abstractmethod
    def defaultConfig():
        return {"x":0, "y":0, "Interval":1}