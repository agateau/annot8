from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PyKDE4.kdecore import *
from PyKDE4.kdeui import *

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
        QObject.connect(self.scene, SIGNAL("selectionChanged()"), self.slotSelectionChanged)

        self.pixmapItem = QGraphicsPixmapItem()
        self.pixmapItem.setZValue(-1)
        self.scene.addItem(self.pixmapItem)

    def createToolBox(self):
        self.toolGroup = QActionGroup(self)
        self.toolGroup.addAction(self.ui.actionSelect)
        self.toolGroup.addAction(self.ui.actionBubble)
        self.toolGroup.addAction(self.ui.actionLine)
        QObject.connect(self.toolGroup, SIGNAL("triggered(QAction*)"), self.slotToolChanged)

        self.ui.toolBar.addSeparator()

        self.colorSelector = KColorButton()
        self.colorSelector.setColor(self.scene.newShapeSettings.pen.color())
        QObject.connect(self.colorSelector, SIGNAL("changed(const QColor&)"), self.slotColorChanged)
        self.ui.toolBar.addWidget(self.colorSelector)

        self.thicknessSelector = QSpinBox()
        self.thicknessSelector.setMinimum(1)
        self.thicknessSelector.setMaximum(16)
        self.thicknessSelector.setValue(self.scene.newShapeSettings.pen.width())
        QObject.connect(self.thicknessSelector, SIGNAL("valueChanged(int)"), self.slotThicknessChanged)
        self.ui.toolBar.addWidget(self.thicknessSelector)


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

    def selectedShapes(self):
        return [self.scene.shapeForItem(x) for x in self.scene.selectedItems()]

    def slotSelectToolRequested(self):
        self.ui.actionSelect.setChecked(True)
        self.slotToolChanged(self.ui.actionSelect)

    def slotSelectionChanged(self):
        shapes = self.selectedShapes()
        color = None
        thickness = None
        if shapes:
            color = shapes[0].settings.pen.color()
            thickness = shapes[0].settings.pen.width()
            for shape in shapes[1:]:
                pen = shape.settings.pen
                if color and pen.color() != color:
                    color = None
                if thickness and pen.width() != thickness:
                    thickness = None
        else:
            color = self.scene.newShapeSettings.pen.color()
            thickness = self.scene.newShapeSettings.pen.width()

        if color:
            self.colorSelector.setColor(color)
        if thickness:
            self.thicknessSelector.setValue(thickness)

    def slotColorChanged(self, color):
        shapes = self.selectedShapes()
        if shapes:
            for shape in shapes:
                shape.settings.setColor(color)
        else:
            self.scene.newShapeSettings.setColor(color)

    def slotThicknessChanged(self, thickness):
        shapes = self.selectedShapes()
        if shapes:
            for shape in shapes:
                shape.settings.setThickness(thickness)
        else:
            self.scene.newShapeSettings.setThickness(thickness)

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
            shape = self.scene.shapeForItem[item]
            self.scene.removeShape(shape)
# vi: ts=4 sw=4 et tw=0
