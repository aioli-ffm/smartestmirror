#!/usr/bin/python
'''
author: Tobias Weis, Christian M
'''
from abc import abstractmethod
from Configurateable import *

from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Base(Configurateable):
    def __init__(self):
        super(Base, self).__init__()
        self.serviceRunner = None

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
        


