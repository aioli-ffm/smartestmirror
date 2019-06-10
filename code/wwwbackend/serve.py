#!/usr/bin/python
from flask import Flask, render_template, request
import json

class configentry(object):
    def __init__(self,name="SomeApp", desc="This app displays stuff"):
        self.name = name
        self.desc = desc 
        self.configs = []

app = Flask(__name__)

@app.route("/")
def index(name="Tobi"):
    configvalues = json.load(open('../mirror/profiles/Default.json'))
    configentries = []

    # FIXME: check if python2 or python3 (iteritems does not exist in py3 anymore)
    for k,v in configvalues.iteritems():
        ce = configentry()
        ce.name = k
        for k2,v2 in v.iteritems():
            ce.configs.append([k2,v2])
        configentries.append(ce)

    return render_template('index.html', configentries=configentries)

@app.route("/handle_data", methods=['POST'])
def handle_data():
    '''
    we get all fields that the app's config-section contained,
    plus an additional field called widget_name,
    which contains the name of the input to match it against the config-file
    '''
    # load original config-file again
    configvalues = json.load(open('../mirror/profiles/Default.json'))

    # get all set fields and put them into the json
    changed_widget_name = request.form['widget_name']
    print "Changed widget: ", changed_widget_name

    for k,v in request.form.iteritems():
	configvalues[changed_widget_name][k] = v

    # write the new values to it
    with open('../mirror/profiles/Default.json', 'w') as outfile:
	json.dump(configvalues, outfile)

    # this needs to return something
    return "bla"
