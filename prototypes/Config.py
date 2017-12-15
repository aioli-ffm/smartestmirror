#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
author: Christian M
'''
import json

class Config(object):
    def __init__(self):
        pass

    def save(self, configurateables, file):
        data = {}
        with open(file, 'w') as outfile:
            for configurateable in configurateables:
                data[configurateable.__class__.__name__] = configurateable.config
            json.dump(data, outfile, indent=4)

    def load(self, configurateables, file):
        data = {}
        with open(file, 'r') as infile:
            data = json.load(infile)
            for configurateable in configurateables:
                configurateable.config = data[configurateable.__class__.__name__]

    def fromJSON(self, configurateable, jsonstr):
        configurateable.config = json.loads(jsonstr)

    def toJSON(self, configurateable):
        return json.dumps(configurateable.config)