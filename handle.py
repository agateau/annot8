from PyQt4.QtCore import *
from PyQt4.QtGui import *

HANDLE_RADIUS = 5

class Handle(QGraphicsEllipseItem):
    def __init__(self, parent, x, y):
        QGraphicsEllipseItem.__init__(self, parent)
        self.linkedItems = []
        self.setRect(-HANDLE_RADIUS, -HANDLE_RADIUS, 2 * HANDLE_RADIUS, 2 * HANDLE_RADIUS)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setPos(x, y)
        self.setBrush(QColor.fromHsvF(0, 0, 1., 0.8))

    def addLinkedItem(self, item):
        self.linkedItems.append(item)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for item in self.linkedItems:
                item.handleMoved(self)
        return QGraphicsEllipseItem.itemChange(self, change, value)

# vi: ts=4 sw=4 et
