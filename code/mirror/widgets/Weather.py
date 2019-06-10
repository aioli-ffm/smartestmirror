#!/usr/bin/python
'''
author: Tobias Weis

you need to get an api-key from openweathermap to use this widget!
'''
import os
import logging
import requests
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from widgets.Base import *

class Weather(QLabel, Base):
    """
    Weather
    """
    def __init__(self, title, parent, serviceRunner):
        super(Weather, self).__init__(title, parent)
        self.parent = parent
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignLeft)
        self.setStyleSheet("color: rgb(255,255,255);")
        self.logger = logging.getLogger(__name__)

    def defaultConfig(self):
        return {"x":50, "y":900, "Interval":600}

    def get_weather(self):
        url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(self.config["location"], self.config["api_key"])
        r = requests.get(url)
        return r.json()

    def parse_weather(self, jo):
        """
        {
            u'clouds': {u'all': 40}, 
            u'name': u'Wiesbaden', 
            u'visibility': 10000, 
            u'sys': 
                {
                u'country': u'DE', 
                u'sunset': 1560195295, 
                u'message': 0.0081, 
                u'type': 1, 
                u'id': 1857, 
                u'sunrise': 1560136682
                }, 
            u'weather': 
                [{
                u'main': u'Clouds', 
                u'id': 802, 
                u'icon': u'03d', 
                u'description': u'scattered clouds'
                }], 
            u'coord': {
                u'lat': 50.08, 
                u'lon': 8.25
                }, 
            u'base': u'stations', 
            u'timezone': 7200, 
            u'dt': 1560170702, 
            u'main': {
                u'pressure': 1013, 
                u'temp_min': 20, 
                u'temp_max': 26.11, 
                u'temp': 22.75, 
                u'humidity': 60}, 
            u'id': 2809346, 
            u'wind': {
                u'speed': 2.6, 
                u'deg': 180}, 
            u'cod': 200}
        """
        retstr = ""
        retstr += "%s<br/>" % jo['name']
        retstr += "%s &deg;C (%s/%s)<br/>" % (jo['main']['temp'], jo['main']['temp_min'], jo['main']['temp_max'])
        retstr += "%s%% humid, %s mb<br/>" % (jo['main']['humidity'], jo['main']['pressure'])


        # http://openweathermap.org/img/w/10d.png
        assert(len(jo['weather']) == 1)
        iconfname = jo['weather'][0]['icon'] + ".png" 
        if not os.path.isfile(os.path.join(self.res_path , iconfname)):
            self.logger.info("Downloading icon " + iconfname)
            iconurl = "http://openweathermap.org/img/w/" + iconfname 
            r = requests.get(iconurl)

            with open(os.path.join(self.res_path, iconfname), 'wb') as f:  
                    f.write(r.content)

        self.logger.debug("Trying to open image with path: " + os.path.join(self.res_path, iconfname))
        retstr +="<img src=\""+os.path.join(self.res_path, iconfname)+"\" /><br/>"

        retstr += "%s - %s" % (jo['weather'][0]['main'], jo['weather'][0]['description'])

        return retstr

    def update(self):
        self.setText("<html>"+self.parse_weather(self.get_weather())+"</html>")
    
