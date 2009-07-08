from PyQt4.QtCore import *
from PyQt4.QtGui import *

from scene import SceneTool

from handle import Handle

class Line(QGraphicsItem):
    def __init__(self):
        QGraphicsItem.__init__(self)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.handles = [Handle(self, 0, 0), Handle(self, 0, 0)]
        self.handles[1].setZValue(self.handles[0].zValue() + 1)
        for handle in self.handles:
            handle.addLinkedItem(self)


    def boundingRect(self):
        return QRectF(self.handles[0].pos(), self.handles[1].pos())


    def paint(self, painter, option, widget):
        painter.drawLine(self.handles[0].pos(), self.handles[1].pos())


    def handleMoved(self, handle):
        self.prepareGeometryChange()


class AddLineTool(SceneTool):
    def __init__(self, scene):
        SceneTool.__init__(self, scene)
        self.item = None


    def mousePressEvent(self, event):
        item = self.scene.itemAt(event.scenePos())
        if isinstance(item, Line):
            return False

        self.item = Line()
        self.scene.addItem(self.item)
        self.item.setPos(event.scenePos())
        return True


    def mouseMoveEvent(self, event):
        if self.item:
            self.item.handles[1].setPos(event.scenePos() - self.item.pos())
            self.item.update()


    def mouseReleaseEvent(self, event):
        self.item = None
        self.scene.emitSelectToolRequested()
# vi: ts=4 sw=4 et
