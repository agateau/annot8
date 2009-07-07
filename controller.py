from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_mainwindow import Ui_MainWindow
from dragwidget import DragWidget
from scene import Scene
from bubble import Bubble
from line import Line

class Controller(QObject):
    def __init__(self):
        QObject.__init__(self)

        self.window = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)

        self.createDragMeWidget()

        self.scene = QGraphicsScene()
        self.ui.view.setScene(self.scene)
        QObject.connect(self.ui.view, SIGNAL("shapeDropped(QString, QPointF)"), self.slotShapeDropped)

        self.pixmapItem = QGraphicsPixmapItem()
        self.pixmapItem.setZValue(-1)
        self.scene.addItem(self.pixmapItem)

        self.createActions()
        for widget in self.ui.bubbleDragWidget, self.ui.lineDragWidget:
            QObject.connect(widget, SIGNAL("dragStarted()"), self.slotShapeDragStarted)

        self.window.resize(700, 500)


    def createDragMeWidget(self):
        dragMeWidget = DragWidget(self.window)
        dragMeWidget.setText(self.tr("Drag Me"))
        self.ui.mainToolBar.addWidget(dragMeWidget)

        QObject.connect(dragMeWidget, SIGNAL("dragStarted()"), self.slotDragStarted)


    def createActions(self):
        QObject.connect(self.ui.actionOpen, SIGNAL("triggered()"), self.open)
        QObject.connect(self.ui.actionSave, SIGNAL("triggered()"), self.save)

        QObject.connect(self.ui.actionDelete, SIGNAL("triggered()"), self.deleteItems)

        QObject.connect(self.ui.actionLine, SIGNAL("triggered()"), self.slotShapeActionTriggered)
        QObject.connect(self.ui.actionBubble, SIGNAL("triggered()"), self.slotShapeActionTriggered)


    def slotDragStarted(self):
        drag = QDrag(self.window)
        mimeData = QMimeData()
        variant = QVariant(self.imageFromScene())
        mimeData.setImageData(variant)
        drag.setMimeData(mimeData)
        drag.start()


    def slotShapeDragStarted(self):
        widget = self.sender()
        classNameFromWidget = {
            self.ui.lineDragWidget: "Line",
            self.ui.bubbleDragWidget: "Bubble",
            }
        className = classNameFromWidget.get(widget)
        if not className:
            return
        drag = QDrag(self.window)
        mimeData = QMimeData()
        mimeData.setText(className)
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
        self.setPixmap(QPixmap(fileName))


    def setPixmap(self, pix):
        self.pixmapItem.setPixmap(pix)
        self.scene.setSceneRect(QRectF(pix.rect()))


    def slotShapeActionTriggered(self):
        action = self.sender()
        shapeFromAction = {
            self.ui.actionBubble: Bubble,
            self.ui.actionLine: Line,
            }

        klass = shapeFromAction.get(action)
        if not klass:
            return
        view = self.ui.view
        pos = QPoint(view.width() / 2, view.height() / 2)
        self.insertShape(klass, pos)


    def slotShapeDropped(self, klassName, pos):
        klass = eval(str(klassName))
        self.insertShape(klass, pos)


    def insertShape(self, klass, pos):
        shape = klass()
        self.scene.addItem(shape)
        shape.setPos(pos)
        view.setFocus()


    def deleteItems(self):
        for item in self.scene.selectedItems():
            self.scene.removeItem(item)
# vi: ts=4 sw=4 et tw=0
