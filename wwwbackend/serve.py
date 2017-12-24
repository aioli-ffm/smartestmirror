#!/usr/bin/python
from flask import Flask, render_template
import json


class configentry(object):
    def __init__(self,name="SomeApp", desc="This app displays stuff"):
        self.name = name
        self.desc = desc 
        self.configs = []

app = Flask(__name__)

@app.route("/")
def hello(name="Tobi"):
    configvalues = json.load(open('../prototypes/Default.json'))
    configentries = []

    # FIXME: check if python2 or python3 (iteritems does not exist in py3 anymore)
    for k,v in configvalues.iteritems():
        ce = configentry()
        ce.name = k
        for k2,v2 in v.iteritems():
            ce.configs.append([k2,v2])
        configentries.append(ce)

    return render_template('index.html', configentries=configentries)
