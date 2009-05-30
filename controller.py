from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_mainwindow import Ui_MainWindow
from dragwidget import DragWidget
from bubble import Bubble

class Controller(QObject):
    def __init__(self):
        QObject.__init__(self)

        self.window = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)

        dragMeWidget = DragWidget(self.tr("Drag Me"), self.window)
        self.ui.mainToolBar.addWidget(dragMeWidget)

        QObject.connect(dragMeWidget, SIGNAL("dragStarted()"), self.slotDragStarted)

        self.scene = QGraphicsScene()
        self.ui.view.setScene(self.scene)

        self.pixmapItem = QGraphicsPixmapItem()
        self.pixmapItem.setZValue(-1)
        self.scene.addItem(self.pixmapItem)

        QObject.connect(self.ui.actionOpen, SIGNAL("triggered()"), self.open)
        QObject.connect(self.ui.actionSave, SIGNAL("triggered()"), self.save)

        QObject.connect(self.ui.actionBubble, SIGNAL("triggered()"), self.addBubble)

        self.window.resize(700, 500)


    def slotDragStarted(self):
        drag = QDrag(self.window)
        mimeData = QMimeData()
        variant = QVariant(self.imageFromScene())
        mimeData.setImageData(variant)
        drag.setMimeData(mimeData)
        drag.start()


    def show(self):
        self.window.show()


    def open(self):
        name = QFileDialog.getOpenFileName(self.window, self.tr("Open Image"))
        if name.isEmpty():
            return
        self.load(name)


    def save(self):
        name = QFileDialog.getSaveFileName(self.window, self.tr("Save Image as"))
        if name.isEmpty():
            return

        image = self.imageFromScene()
        image.save(name, "PNG")


    def imageFromScene(self):
        rect = self.scene.itemsBoundingRect()
        image = QImage(int(rect.width()), int(rect.height()), QImage.Format_ARGB32)
        image.fill(Qt.transparent)
        painter = QPainter(image)
        self.scene.render(painter, rect, rect)
        painter.end()
        return image


    def load(self, fileName):
        pix = QPixmap(fileName)
        self.pixmapItem.setPixmap(pix)
        self.scene.setSceneRect(QRectF(pix.rect()))


    def addBubble(self):
        bubble = Bubble("A Bubble")
        rect = self.pixmapItem.boundingRect()
        bubble.setPos(rect.width() / 2, rect.height() / 2)
        self.scene.addItem(bubble)


# vi: ts=4 sw=4 et tw=0
