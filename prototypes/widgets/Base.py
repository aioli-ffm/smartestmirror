#!/usr/bin/python
'''
author: Tobias Weis
'''
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Base(object):
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
        


