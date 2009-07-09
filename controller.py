from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_mainwindow import Ui_MainWindow
from dragwidget import DragWidget
from scene import Scene
from bubble import AddBubbleTool
from line import AddLineTool

class Controller(QObject):
    def __init__(self):
        QObject.__init__(self)

        self.window = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)

        self.createDragMeWidget()
        self.createScene()
        self.createActions()
        self.createToolBox()

        self.window.resize(700, 500)

    def createScene(self):
        self.scene = Scene()
        self.ui.view.setScene(self.scene)
        QObject.connect(self.scene, SIGNAL("selectToolRequested()"), self.slotSelectToolRequested)

        self.pixmapItem = QGraphicsPixmapItem()
        self.pixmapItem.setZValue(-1)
        self.scene.addItem(self.pixmapItem)

    def createToolBox(self):
        self.toolGroup = QActionGroup(self)
        self.toolGroup.addAction(self.ui.actionSelect)
        self.toolGroup.addAction(self.ui.actionBubble)
        self.toolGroup.addAction(self.ui.actionLine)
        QObject.connect(self.toolGroup, SIGNAL("triggered(QAction*)"), self.slotToolChanged)


    def createDragMeWidget(self):
        dragMeWidget = DragWidget(self.tr("Drag Me"), self.window)
        self.ui.mainToolBar.addWidget(dragMeWidget)

        QObject.connect(dragMeWidget, SIGNAL("dragStarted()"), self.slotDragStarted)


    def createActions(self):
        QObject.connect(self.ui.actionOpen, SIGNAL("triggered()"), self.open)
        QObject.connect(self.ui.actionSave, SIGNAL("triggered()"), self.save)

        QObject.connect(self.ui.actionDelete, SIGNAL("triggered()"), self.deleteItems)


    def slotDragStarted(self):
        drag = QDrag(self.window)
        mimeData = QMimeData()
        variant = QVariant(self.imageFromScene())
        mimeData.setImageData(variant)
        drag.setMimeData(mimeData)
        drag.start()

    def slotSelectToolRequested(self):
        self.ui.actionSelect.setChecked(True)
        self.slotToolChanged(self.ui.actionSelect)

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


    def slotToolChanged(self, action):
        toolFromAction = {
            self.ui.actionBubble: AddBubbleTool,
            self.ui.actionLine: AddLineTool,
            }

        klass = toolFromAction.get(action)
        if klass:
            tool = klass(self.scene)
        else:
            tool = None
        self.scene.setTool(tool)


    def deleteItems(self):
        for item in self.scene.selectedItems():
            self.scene.removeItem(item)
# vi: ts=4 sw=4 et tw=0
