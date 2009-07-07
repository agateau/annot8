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


class Line(QGraphicsItem):
    def __init__(self):
        QGraphicsItem.__init__(self)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.handles = [Handle(self, 0, 0), Handle(self, 40, 30)]
        self.handles[1].setZValue(self.handles[0].zValue() + 1)

        self.inited = False


    def boundingRect(self):
        return QRectF(self.handles[0].pos(), self.handles[1].pos())


    def paint(self, painter, option, widget):
        if not self.inited:
            for handle in self.handles:
                handle.installSceneEventFilter(self)
            self.inited = True

        painter.drawLine(self.handles[0].pos(), self.handles[1].pos())


    def sceneEventFilter(self, item, event):
        if event.type() == QEvent.GraphicsSceneMouseMove:
            self.prepareGeometryChange()
        return False
# vi: ts=4 sw=4 et
