#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import datetime

class Button(QPushButton):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.parent = parent
        
    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.RightButton:
            return

        mimeData = QMimeData()

        self.parent.current_drag = self
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        
        if e.button() == Qt.LeftButton:
            print('press')

class Text(QLabel):
    def __init__(self, title, parent):
        super().__init__(title,parent)
        self.parent = parent
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def settext(self,text):
        self.setText(text)
        self.setStyleSheet("color: rgb(255,255,255);")

        f = self.font()
        m = QFontMetrics(f)
        size = m.size(0, self.text())
        print(size.width())
        #self.resize(size.width(), size.height())
        #self.setGeometry(self.x(), self.y(), size.width(), size.height())
        self.setFixedSize(size.width(), size.height())


        #self.adjustSize()
        #self.updateGeometry()
        #self.parent.updateGeometry()

    def update(self):
        print("Update called")
        print(str(datetime.datetime.now().time()))
        self.settext(str(datetime.datetime.now().time()))

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.RightButton:
            return

        mimeData = QMimeData()

        self.parent.current_drag = self
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)


class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_drag = None
        
    def initUI(self):
        self.setAcceptDrops(True)

        # create window, geometry and colors
        self.setWindowTitle('Smartestmirror')
        self.setGeometry(0, 0, 1920, 1080)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        # add elements to canvas
        self.button = Button('Button', self)
        self.button.move(100, 65)

        self.text_time = Text('Timer', self)
        self.text_time.settext("Test")
        self.text_time.move(500,200)

        # set timers for update functions
        self.timer = QTimer()
        self.timer.timeout.connect(self.text_time.update)
        self.timer.start(1000)


    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        position = e.pos()
        self.current_drag.move(position)
        #self.button.move(position)

        e.setDropAction(Qt.MoveAction)
        e.accept()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Canvas()
    ex.show()
    app.exec_() 
