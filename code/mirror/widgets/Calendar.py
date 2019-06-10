#!/usr/bin/python
'''
author: Christian M
'''
from __future__ import print_function, unicode_literals
import httplib2
import os
from apiclient import discovery
from oauth2client import client, tools, file
from httplib2 import Http
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
# https://console.developers.google.com/apis/credentials?project=coral-firefly-192215

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

class Calendar(QLabel, Base):

    labeltext = ''
    """
    Display Google Calendar
    """

    def __init__(self, title, parent, serviceRunner):
        super(Calendar, self).__init__(title, parent)
        self.parent = parent
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignLeft)
        self.setStyleSheet("color: rgb(255,255,255);")

    def defaultConfig(self):
        return {"x": 50, "y": 900, "Interval": 10, "credentials_file": "./profiles/credentials_calendar.json", "calendar": "primary", "results": 3}

    def init(self):
        try:
            store = file.Storage("token.json")
            creds = store.get()

            if not creds or creds.invalid:
                flow = client.flow_from_clientsecrets(self.config['credentials_file'], SCOPES)
                creds = tools.run_flow(flow, store)
            self.service = discovery.build('calendar', 'v3', http=creds.authorize(Http()))
        except Exception, e:
            print('[Exception Calendar Widget', e)

    def settext(self, text):
        self.setText(text)
        newfont = QFont("Times", 14, QFont.Bold)
        self.setFont(newfont)

        f = self.font()
        m = QFontMetrics(f)
        size = m.size(0, self.text())
        self.setFixedSize(size.width(), size.height())

    def setevents(self, events):
        if not events:
            self.labeltext = 'No upcoming events found.'
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            date = start.split("T")[0]
            try:
                time = (":").join(start.split("T")[1].split("+")[0].split(":")[:-1])
            except:
                # maybe whole day, so no time given!
                time = ""

            self.labeltext = self.labeltext + \
                str(date) + ', ' +time + ', ' + event['summary']
            self.labeltext = self.labeltext + '\n'

    def updatecalendar(self):
        try:
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            eventsResult = self.service.events().list(
                calendarId=self.config['calendar'], timeMin=now, maxResults=self.config["results"], singleEvents=True,
                orderBy='startTime').execute()
            events = eventsResult.get('items', [])

            self.setevents(events)
        except Exception, e:
            print('[Exception Calendar Widget', e)

    def update(self):
        self.labeltext = ''
        self.updatecalendar()
        self.settext(self.labeltext)
