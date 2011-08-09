from PyQt4.QtCore import *
from PyQt4.QtGui import *

HANDLE_RADIUS = 5

class Handle(QGraphicsObject):
    moved = pyqtSignal(QGraphicsObject)

    def __init__(self, parent, x, y):
        QGraphicsObject.__init__(self, parent)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setPos(x, y)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            self.moved.emit(self)
        return QGraphicsObject.itemChange(self, change, value)

    def paint(self, painter, options, widgets):
        painter.setBrush(QColor.fromHsvF(0, 0, 1., 0.8))
        painter.drawEllipse(self.boundingRect())

    def boundingRect(self):
        return QRectF(-HANDLE_RADIUS, -HANDLE_RADIUS, 2 * HANDLE_RADIUS, 2 * HANDLE_RADIUS)

# vi: ts=4 sw=4 et
