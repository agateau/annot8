from PyQt4.QtCore import *
from PyQt4.QtGui import *

DRAG_MIN_SIZE = 10

class DragWidget(QLabel):
    def __init__(self, parent):
        QLabel.__init__(self, parent)
        self.setCursor(Qt.OpenHandCursor)
        self.clickPoint = QPoint(0, 0)
        self.setStyleSheet("background-color: palette(base); border: 1px solid palette(mid); border-radius: 6px")


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clickPoint = QPoint(event.pos())


    def mouseMoveEvent(self, event):
        delta = event.pos() - self.clickPoint
        if self.clickPoint != QPoint(0, 0) \
            and delta.manhattanLength() > DRAG_MIN_SIZE:
            self.clickPoint = event.pos()
            self.emit(SIGNAL("dragStarted()"), ())


    def mouseReleaseEvent(self, event):
        self.clickPoint = QPoint(0, 0)

# vi: ts=4 sw=4 et tw=0
