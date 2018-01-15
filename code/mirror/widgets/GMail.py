#!/usr/bin/python
'''
author: Christian M
'''
from __future__ import print_function, unicode_literals
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import calendar
from widgets.Base import *
import json
import requests

# https://developers.google.com/google-apps/calendar/quickstart/python


class GMail(QLabel, Base):

    service = None

    """
    Display GMail and Calendar
    """

    def __init__(self, title, parent, serviceRunner):
        super(GMail, self).__init__(title, parent)
        self.parent = parent
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("color: rgb(255,255,255);")

    def defaultConfig(self):
        return {"x": 50, "y": 900, "Interval": 10, "api_key": "XXXXX", "calendar": "primary", "results":3}

    def init(self):
        self.service = discovery.build('calendar', 'v3', developerKey=self.config["api_key"])

    def settext(self, text):
        self.setText(text)
        newfont = QFont("Times", 22, QFont.Bold)
        self.setFont(newfont)

        f = self.font()
        m = QFontMetrics(f)
        size = m.size(0, self.text())
        self.setFixedSize(size.width(), size.height())

    def setevents(self, events):
        text = ''
        if not events:
            text = 'No upcoming events found.'
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            text = text + str(start) + ' ' + event['summary']
            text = text + '\n'
        self.settext(text)

    def update(self):
        try:
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            eventsResult = self.service.events().list(
                calendarId=self.config['calendar'], timeMin=now, maxResults=self.config["results"], singleEvents=True,
                orderBy='startTime').execute()
            events = eventsResult.get('items', [])

            self.setevents(events)
        except Exception,e:
            print('exception in GMail module',e) 

