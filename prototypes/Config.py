#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
author: Christian M
'''
import json

class Config(object):
    def __init__(self):
        pass

    def save(self, path):
        pass

    def load(self, path):
        pass

    def fromJSON(self, configurateable, jsonstr):
        configurateable.config = json.loads(jsonstr)

    def toJSON(self, configurateable):
        return json.dumps(configurateable.config)