from PyQt4.QtCore import *
from PyQt4.QtGui import *


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


class Scene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
        self._tool = None

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

# vi: ts=4 sw=4 et tw=0
