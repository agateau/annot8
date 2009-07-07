from PyQt4.QtCore import *
from PyQt4.QtGui import *

from bubble import Bubble
from line import Line

class GraphicsView(QGraphicsView):
    def dragEnterEvent(self, event):
        QGraphicsView.dragEnterEvent(self, event)
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        QGraphicsView.dragMoveEvent(self, event)
        event.acceptProposedAction()

    def dropEvent(self, event):
        klassName = event.mimeData().text()
        pos = self.mapToScene(event.pos())
        self.emit(SIGNAL("shapeDropped(QString, QPointF)"), klassName, pos)
# vi: ts=4 sw=4 et tw=0
