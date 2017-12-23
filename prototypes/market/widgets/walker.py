#!/usr/bin/python
'''
author: Christian M
'''
from os import walk
from os.path import basename, splitext
import json

def all(path):
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        for file in filenames:
            if file.endswith(".json"):
                f.append(splitext(basename(file))[0])
        break
    return f

def load(file):
        data = {
            "title":"Widget not found",
            "description":"unknown",
            "value":0
        }
        with open(file, 'r') as infile:
            print(file)
            data = json.load(infile)
        return data

def widget(path):
    return load(path)