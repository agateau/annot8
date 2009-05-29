from PyQt4.QtCore import *
from PyQt4.QtGui import *

from toolbar import ToolBar
from bubble import Bubble

class Controller(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.pixmapItem = QGraphicsPixmapItem()
        self.pixmapItem.setZValue(-1)
        self.scene.addItem(self.pixmapItem)

        self.shapeToolBar = ToolBar(Qt.Vertical)
        self.shapeToolBar.setZValue(1)
        self.shapeToolBar.addTool("bubble", self.addBubble)
        self.scene.addItem(self.shapeToolBar)
        self.shapeToolBar.setPos(0, 0)


    def show(self):
        self.view.show()


    def load(self, fileName):
        pix = QPixmap(fileName)
        self.pixmapItem.setPixmap(pix)
        self.view.resize(pix.size())


    def addBubble(self):
        bubble = Bubble("A Bubble")
        bubble.setPos(self.view.width() / 2, self.view.height() / 2)
        self.scene.addItem(bubble)


# vi: ts=4 sw=4 et
