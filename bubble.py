import math

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from scene import SceneTool
from shape import Shape
from handle import Handle

OPACITY = 0.8
MARGIN = 10

ANCHOR_THICKNESS = 20

def computeAnchorDelta(vector, length):
    if vector.x() != 0:
        angle = math.atan(vector.y() / vector.x())
    else:
        angle = math.pi / 2
    angle += math.pi / 2
    return QPointF(length * math.cos(angle), length * math.sin(angle))

class BubbleItem(QGraphicsPathItem):
    def __init__(self, shape):
        QGraphicsPathItem.__init__(self)
        self.shape = shape

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSceneHasChanged:
            self.shape.textItem.setFocus()
        elif change == QGraphicsItem.ItemSelectedHasChanged:
            selected = value.toBool()
            if selected:
                self.shape.textItem.setFocus()
            self.shape.setHandlesVisible(selected)
        return QGraphicsPathItem.itemChange(self, change, value)


class BubbleShape(Shape):
    def __init__(self):
        Shape.__init__(self, BubbleItem(self))
        self.item.setFlag(QGraphicsItem.ItemIsSelectable)

        self.item.setBrush(QColor.fromHsvF(0, 0, 1., OPACITY))

        self.anchorHandle = Handle(self.item, 0, 0)
        # Position the bubble to the right of the anchor so that it can grow
        # vertically without overflowing the anchor
        self.bubbleHandle = Handle(self.item, ANCHOR_THICKNESS, -ANCHOR_THICKNESS)
        self.anchorHandle.addLinkedShape(self)
        self.bubbleHandle.addLinkedShape(self)

        self.setHandlesVisible(False)

        self.textItem = QGraphicsTextItem(self.item)
        self.textItem.setTextInteractionFlags(Qt.TextEditorInteraction)
        QObject.connect(self.textItem.document(), SIGNAL("contentsChanged()"), \
            self.adjustSizeFromText)
        self.textItem.setPlainText("")

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

        # Compute anchor polygon
        center = rect.center()
        delta = computeAnchorDelta(center - self.anchorHandle.pos(), ANCHOR_THICKNESS / 2)

        anchor = QPolygonF([
            self.anchorHandle.pos(),
            center + delta,
            center - delta])

        # Avoid blurry borders
        anchor.translate(0.5, 0.5)
        rect.translate(0.5, 0.5)

        polygon = anchor.united(QPolygonF(rect))
        path = QPainterPath()
        path.addPolygon(polygon)
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
