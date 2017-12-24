#!/usr/bin/python
from flask import Flask, render_template

class configentry(object):
    def __init__(self,name="SomeApp", desc="This app displays stuff"):
        self.name = name
        self.desc = desc 
        self.x = 10
        self.y = 20

configentries = [
        configentry('Widget1', 'This app displays some nice stuff, pictures and comics and shit'), 
        configentry('Widget2', 'This app does nothing, it only uses up compute-cycles.')
        ]

app = Flask(__name__)

@app.route("/")
def hello(name="Tobi"):
    return render_template('index.html', configentries=configentries)
