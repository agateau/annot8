from PyQt4.QtCore import *
from PyQt4.QtGui import *

from scene import SceneTool
from shape import Shape
from handle import Handle

class LineItem(QGraphicsLineItem):
    def __init__(self, shape):
        QGraphicsLineItem.__init__(self)
        self.shape = shape

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSceneHasChanged:
            self.shape.settings.pen = QPen(self.scene().newShapeSettings.pen)
            self.shape.updatePen()
        elif change == QGraphicsItem.ItemSelectedHasChanged:
            selected = value.toBool()
            self.shape.setHandlesVisible(selected)
        return QGraphicsLineItem.itemChange(self, change, value)


class LineShape(Shape):
    def __init__(self):
        Shape.__init__(self, LineItem(self))
        self.item.setFlag(QGraphicsItem.ItemIsSelectable)

        self.handles.append(Handle(self.item, 0, 0))
        self.handles.append(Handle(self.item, 0, 0))
        self.handles[1].setZValue(self.handles[0].zValue() + 1)
        for handle in self.handles:
            handle.addShape(self)
        self.setHandlesVisible(False)

    def updatePen(self):
        pen = QPen(self.settings.pen)
        pen.setCapStyle(Qt.RoundCap)
        self.item.setPen(pen)

    def handleMoved(self, handle):
        self.item.setLine(QLineF(self.handles[0].pos(), self.handles[1].pos()))

    def settingsChanged(self):
        self.updatePen()


class AddLineTool(SceneTool):
    def __init__(self, scene):
        SceneTool.__init__(self, scene)
        self.shape = None


    def mousePressEvent(self, event):
        item = self.scene.itemAt(event.scenePos())
        if isinstance(item, LineShape):
            return False

        self.shape = LineShape()
        self.scene.addShape(self.shape)
        self.shape.item.setPos(event.scenePos())
        self.shape.item.setSelected(True)
        return True


    def mouseMoveEvent(self, event):
        if self.shape:
            self.shape.handles[1].setPos(event.scenePos() - self.shape.item.pos())
            # FIXME: Necessary?
            self.shape.item.update()


    def mouseReleaseEvent(self, event):
        self.shape = None
        self.scene.emitSelectToolRequested()
# vi: ts=4 sw=4 et
