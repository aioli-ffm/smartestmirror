#!/usr/bin/python
'''
author: Tobias Weis, Christian M
'''
from abc import abstractmethod
import logging
#from Configurateable import *

from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Base(object):
    def __init__(self):
        super(Base, self).__init__()
        self.serviceRunner = None
        self.res_path = None #resources-directory
        self.config = {}
        self.logger = logging.getLogger(__name__)

    @classmethod
    @abstractmethod
    def defaultConfig(self):
        return {"x":0, "y":0, "Interval":1}

    @classmethod
    @abstractmethod
    def init(self):
        pass

    @classmethod
    @abstractmethod
    def update(self):
        pass

    """ 
    Implement draggabe for all widgets
    """
    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.RightButton:
            return

        mimeData = QMimeData()

        self.parent.current_drag = self
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)
        


