from PyQt4.QtCore import *
from PyQt4.QtGui import *

from shapesettings import ShapeSettings

class SceneTool(QObject):
    def __init__(self, scene):
        QObject.__init__(self)
        self.scene = scene

    def mouseMoveEvent(self, event):
        return False

    def mousePressEvent(self, event):
        return False

    def mouseReleaseEvent(self, event):
        return False

DEFAULT_COLOR = QColor.fromRgbF(1, 0, 0, 0.8)
DEFAULT_THICKNESS = 4

class Scene(QGraphicsScene):
    __slots__ = ["_tool", "_newShapeSettings"]
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
        self._shapeForItem = {}
        self._tool = None
        self._newShapeSettings = ShapeSettings()
        self._newShapeSettings.pen = QPen(DEFAULT_COLOR, DEFAULT_THICKNESS)

    @property
    def newShapeSettings(self):
        return self._newShapeSettings

    def shapeForItem(self, item):
        return self._shapeForItem[item]

    def emitSelectToolRequested(self):
        self.emit(SIGNAL("selectToolRequested()"))

    def setTool(self, tool):
        self._tool = tool

    def mouseMoveEvent(self, event):
        if not self._tool or not self._tool.mouseMoveEvent(event):
            QGraphicsScene.mouseMoveEvent(self, event)

    def mousePressEvent(self, event):
        if not self._tool or not self._tool.mousePressEvent(event):
            QGraphicsScene.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        if not self._tool or not self._tool.mouseReleaseEvent(event):
            QGraphicsScene.mouseReleaseEvent(self, event)

    def addShape(self, shape):
        self._shapeForItem[shape.item] = shape
        self.addItem(shape.item)

    def removeShape(self, shape):
        self.removeItem(shape.item)
        del self._shapeForItem[shape.item]
# vi: ts=4 sw=4 et tw=0
