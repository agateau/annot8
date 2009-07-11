from PyQt4.QtCore import *
from PyQt4.QtGui import *

class ShapeSettings(object):
    __slots__ = ["_pen", "_brush", "_callBack"]
    def __init__(self, callBack=None):
        self._pen = QPen()
        self._brush = QBrush()
        self._callBack = callBack

    @property
    def pen(self):
        return self._pen

    @pen.setter
    def pen(self, value):
        self._pen = value
        if self._callBack:
            self._callBack()

    @property
    def brush(self):
        return self._brush

    @brush.setter
    def brush(self, value):
        self._brush = value
        if self._callBack:
            self._callBack()

    def setColor(self, value):
        self._pen.setColor(value)
        if self._callBack:
            self._callBack()

    def setThickness(self, value):
        self._pen.setWidth(value)
        if self._callBack:
            self._callBack()
# vi: ts=4 sw=4 et
