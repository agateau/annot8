from PyQt4.QtCore import *
from PyQt4.QtGui import *

from scene import SceneTool

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

        self.handles = [Handle(self, 0, 0), Handle(self, 0, 0)]
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
# vi: ts=4 sw=4 et
