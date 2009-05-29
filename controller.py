from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_mainwindow import Ui_MainWindow
from bubble import Bubble

class Controller(QObject):
    def __init__(self):
        QObject.__init__(self)

        self.window = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)

        self.scene = QGraphicsScene()
        self.ui.view.setScene(self.scene)

        self.pixmapItem = QGraphicsPixmapItem()
        self.pixmapItem.setZValue(-1)
        self.scene.addItem(self.pixmapItem)

        QObject.connect(self.ui.actionBubble, SIGNAL("triggered()"), \
            self.addBubble)

        self.window.resize(700, 500)


    def show(self):
        self.window.show()


    def load(self, fileName):
        pix = QPixmap(fileName)
        self.pixmapItem.setPixmap(pix)
        self.scene.setSceneRect(QRectF(pix.rect()))


    def addBubble(self):
        bubble = Bubble("A Bubble")
        rect = self.pixmapItem.boundingRect()
        bubble.setPos(rect.width() / 2, rect.height() / 2)
        self.scene.addItem(bubble)


# vi: ts=4 sw=4 et
