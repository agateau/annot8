import math

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from scene import SceneTool
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

class Bubble(QGraphicsPathItem):
    def __init__(self):
        QGraphicsPathItem.__init__(self)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.setBrush(QColor.fromHsvF(0, 0, 1., OPACITY))

        self.anchorHandle = Handle(self, 0, 0)
        self.bubbleHandle = Handle(self, -ANCHOR_THICKNESS, ANCHOR_THICKNESS)
        self.anchorHandle.addLinkedItem(self)
        self.bubbleHandle.addLinkedItem(self)

        self.setHandlesVisible(False)

        self.text = QGraphicsTextItem(self)
        self.text.setTextInteractionFlags(Qt.TextEditorInteraction)
        QObject.connect(self.text.document(), SIGNAL("contentsChanged()"), \
            self.adjustSizeFromText)
        self.text.setPlainText("")

    def adjustSizeFromText(self):
        # Place bubble rect above bubbleHandle
        self.text.adjustSize()
        textSize = self.text.document().size()
        rect = QRectF(self.bubbleHandle.pos(), textSize)
        rect.adjust(0, 0, 2*MARGIN, 2*MARGIN)

        minWidth = 2*MARGIN + ANCHOR_THICKNESS
        if rect.width() < minWidth:
            rect.setWidth(minWidth)

        # Position text in bubble rect
        self.text.setPos(rect.left() + MARGIN, rect.top() + MARGIN)

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
        self.setPath(path)


    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSceneHasChanged:
            self.text.setFocus()
        elif change == QGraphicsItem.ItemSelectedHasChanged:
            selected = value.toBool()
            if selected:
                self.text.setFocus()
            self.setHandlesVisible(selected)
        return QGraphicsPathItem.itemChange(self, change, value)


    def handleMoved(self, handle):
        self.adjustSizeFromText()


    def setHandlesVisible(self, visible):
        if visible:
            opacity = 1
        else:
            opacity = 0
        self.bubbleHandle.setVisible(visible)
        self.anchorHandle.setVisible(visible)


class AddBubbleTool(SceneTool):
    def mousePressEvent(self, event):
        item = self.scene.itemAt(event.scenePos())
        if isinstance(item, Bubble):
            return False

        bubble = Bubble()
        self.scene.addItem(bubble)
        bubble.setPos(event.scenePos())
        bubble.setSelected(True)
        return True
# vi: ts=4 sw=4 et
