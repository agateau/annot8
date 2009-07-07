from PyQt4.QtCore import *
from PyQt4.QtGui import *

from handle import Handle

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
