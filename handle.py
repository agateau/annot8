from PyQt4.QtCore import *
from PyQt4.QtGui import *

HANDLE_RADIUS = 5

class Handle(QGraphicsEllipseItem):
    def __init__(self, parent, x, y):
        QGraphicsEllipseItem.__init__(self, parent)
        self.setRect(-HANDLE_RADIUS, -HANDLE_RADIUS, 2 * HANDLE_RADIUS, 2 * HANDLE_RADIUS)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setPos(x, y)
        self.setBrush(QColor.fromHsvF(0, 0, 1., 0.8))
