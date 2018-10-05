#!/usr/bin/python
'''
author: Christian M
'''
from __future__ import print_function, unicode_literals
import httplib2
import os
import imaplib
import email, email.Header
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
# https://console.developers.google.com/apis/credentials?project=coral-firefly-192215


class Mail(QLabel, Base):

    mail_service = None
    labeltext = ''
    """
    Display IMAP Mail
    """

    def __init__(self, title, parent, serviceRunner):
        super(Mail, self).__init__(title, parent)
        self.parent = parent
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("color: rgb(255,255,255);")

    def defaultConfig(self):
        return {"x": 50, "y": 900, "Interval": 10, "server": "localhost", "port": 993, "username":"username", "password":"password", "results": 3, "mailbox":"Inbox"}

    def init(self):
        try:
            self.mail_service = imaplib.IMAP4_SSL(host=self.config["server"], port=self.config["port"])
            self.mail_service.login(self.config["username"], self.config["password"])
            self.mail_service.select(self.config["mailbox"])
        except Exception, e:
            print('exception in login', e)

    def settext(self, text):
        self.setText(text)
        newfont = QFont("Times", 22, QFont.Bold)
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
            self.labeltext = self.labeltext + \
                str(start) + ' ' + event['summary']
            self.labeltext = self.labeltext + '\n'

    def setmails(self, messages):
        if not messages:
            self.labeltext = 'No messages found.'
        for message in messages:
            self.labeltext = self.labeltext + message
            self.labeltext = self.labeltext + '\n'

    def updatemails(self):
        try:
            typ, data = self.mail_service.sort('REVERSE DATE', 'UTF-8', 'ALL')
            mails = []
            for num in data[0].split()[:(self.config["results"]-1)]:
                typ, data = self.mail_service.fetch(num, '(RFC822)')
                
                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_string(response_part[1])
                        subject = msg['subject']
                        #if subject.startswith('='):
                        #    subject, encoding = email.Header.decode_header(subject)[0]
                        mails.append(subject)
            self.setmails(mails)
        except Exception, e:
            print('[Exception Mail Widget] ', e)

    def update(self):
        self.labeltext = ''
        self.updatemails()
        self.settext(self.labeltext)
