from PyQt4.QtCore import *
from PyQt4.QtGui import *

from scene import SceneTool

from handle import Handle

DEFAULT_THICKNESS = 4
DEFAULT_COLOR = QColor.fromRgbF(1, 0, 0, 0.8)

class Line(QGraphicsLineItem):
    def __init__(self):
        QGraphicsLineItem.__init__(self)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        pen = QPen(DEFAULT_COLOR, DEFAULT_THICKNESS)
        pen.setCapStyle(Qt.RoundCap)
        self.setPen(pen)

        self.handles = [Handle(self, 0, 0), Handle(self, 0, 0)]
        self.handles[1].setZValue(self.handles[0].zValue() + 1)
        for handle in self.handles:
            handle.addLinkedItem(self)
        self.setHandlesVisible(False)

    def handleMoved(self, handle):
        self.setLine(QLineF(self.handles[0].pos(), self.handles[1].pos()))

    def setHandlesVisible(self, visible):
        for handle in self.handles:
            handle.setVisible(visible)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedHasChanged:
            selected = value.toBool()
            self.setHandlesVisible(selected)
        return QGraphicsLineItem.itemChange(self, change, value)


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
        self.item.setSelected(True)
        return True


    def mouseMoveEvent(self, event):
        if self.item:
            self.item.handles[1].setPos(event.scenePos() - self.item.pos())
            self.item.update()


    def mouseReleaseEvent(self, event):
        self.item = None
        self.scene.emitSelectToolRequested()
# vi: ts=4 sw=4 et
