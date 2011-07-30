import math

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from scene import SceneTool
from shape import Shape
from handle import Handle

OPACITY = 0.8
MARGIN = 10

ANCHOR_THICKNESS = 20

def computeAnchorPolygon(center, anchorPos):
    length = ANCHOR_THICKNESS / 2
    vector = anchorPos - center
    if vector.x() != 0:
        angle = math.atan(vector.y() / vector.x())
    else:
        angle = math.pi / 2
    angle += math.pi / 2
    delta = QPointF(length * math.cos(angle), length * math.sin(angle))

    return QPolygonF([
        anchorPos,
        center + delta,
        center - delta])

class BubbleItem(QGraphicsPathItem):
    def __init__(self, shape):
        QGraphicsPathItem.__init__(self)
        self.shape = shape

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSceneHasChanged:
            self.shape.textItem.setFocus()
        elif change == QGraphicsItem.ItemSelectedHasChanged:
            selected = value.toBool()
            self.shape.setHandlesVisible(selected)
        return QGraphicsPathItem.itemChange(self, change, value)


class BubbleShape(Shape):
    def __init__(self):
        def initHandle(handle):
            handle.addLinkedShape(self)
            handle.setFlag(QGraphicsItem.ItemIsFocusable)
            handle.setFocusProxy(self.textItem)

        Shape.__init__(self, BubbleItem(self))
        # Item
        self.item.setFlag(QGraphicsItem.ItemIsSelectable)
        self.item.setFlag(QGraphicsItem.ItemIsFocusable)

        self.item.setBrush(QColor.fromHsvF(0, 0, 1., OPACITY))

        # Text item
        self.textItem = QGraphicsTextItem(self.item)
        self.textItem.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.item.setFocusProxy(self.textItem)
        QObject.connect(self.textItem.document(), SIGNAL("contentsChanged()"), \
            self.adjustSizeFromText)

        # Handles
        self.anchorHandle = Handle(self.item, 0, 0)
        # Position the bubble to the right of the anchor so that it can grow
        # vertically without overflowing the anchor
        self.bubbleHandle = Handle(self.item, ANCHOR_THICKNESS, -ANCHOR_THICKNESS)
        initHandle(self.anchorHandle)
        initHandle(self.bubbleHandle)
        self.setHandlesVisible(False)

        self.adjustSizeFromText()

    def adjustSizeFromText(self):
        # Place bubble rect above bubbleHandle
        self.textItem.adjustSize()
        textSize = self.textItem.document().size()
        rect = QRectF(self.bubbleHandle.pos(), textSize)
        rect.adjust(0, 0, 2*MARGIN, 2*MARGIN)

        minWidth = 2*MARGIN + ANCHOR_THICKNESS
        if rect.width() < minWidth:
            rect.setWidth(minWidth)

        # Position text in bubble rect
        self.textItem.setPos(rect.left() + MARGIN, rect.top() + MARGIN)

        # Compute polygon
        anchorPolygon = computeAnchorPolygon(rect.center(), self.anchorHandle.pos())
        polygon = anchorPolygon.united(QPolygonF(rect))
        path = QPainterPath()
        path.addPolygon(polygon)
        path.translate(0.5, 0.5)
        self.item.setPath(path)

    def handleMoved(self, handle):
        self.adjustSizeFromText()

    def setHandlesVisible(self, visible):
        self.bubbleHandle.setVisible(visible)
        self.anchorHandle.setVisible(visible)


class AddBubbleTool(SceneTool):
    def mousePressEvent(self, event):
        item = self.scene.itemAt(event.scenePos())
        if isinstance(item, BubbleShape):
            return False

        bubble = BubbleShape()
        self.scene.addShape(bubble)
        bubble.item.setPos(event.scenePos())
        bubble.item.setSelected(True)

        self.scene.emitSelectToolRequested()
        return True
# vi: ts=4 sw=4 et
