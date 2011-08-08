from PyQt4.QtCore import *
from PyQt4.QtGui import *

class ShapeAccessoryItem(QGraphicsItemGroup):
    __slots__ = ["_shapes"]
    """
    Item which is associated with shapes
    """
    def __init__(self, parent):
        QGraphicsItemGroup.__init__(self, parent)
        self._shapes = []

    @property
    def shapes(self):
        return self._shapes

    def addShape(self, shape):
        self._shapes.append(shape)
# vi: ts=4 sw=4 et
