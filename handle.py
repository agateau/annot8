from PyQt4.QtCore import *
from PyQt4.QtGui import *

from shapeaccessoryitem import ShapeAccessoryItem

HANDLE_RADIUS = 5

class EllipseItem(QGraphicsEllipseItem):
    def __init__(self, parent):
        QGraphicsEllipseItem.__init__(self, parent)
        self.setRect(-HANDLE_RADIUS, -HANDLE_RADIUS, 2 * HANDLE_RADIUS, 2 * HANDLE_RADIUS)
        self.setBrush(QColor.fromHsvF(0, 0, 1., 0.8))


class Handle(ShapeAccessoryItem):
    def __init__(self, parent, x, y):
        ShapeAccessoryItem.__init__(self, parent)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setPos(x, y)
        self.ellipseItem = EllipseItem(self)
        self.addToGroup(self.ellipseItem)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for shape in self.shapes:
                shape.handleMoved(self)
        return ShapeAccessoryItem.itemChange(self, change, value)

# vi: ts=4 sw=4 et
