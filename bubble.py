from PyQt4.QtCore import *
from PyQt4.QtGui import *

from scene import SceneTool

OPACITY = 0.8
MARGIN = 10

ANCHOR_WIDTH = 20
ANCHOR_HEIGHT = 20

class Bubble(QGraphicsPathItem):
    def __init__(self):
        QGraphicsPathItem.__init__(self)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.setBrush(QColor.fromHsvF(0, 0, 1., OPACITY))

        self.text = QGraphicsTextItem(self)
        self.text.setTextInteractionFlags(Qt.TextEditorInteraction)
        QObject.connect(self.text.document(), SIGNAL("contentsChanged()"), \
            self.adjustSizeFromText)
        self.text.setPlainText("")

    def adjustSizeFromText(self):
        # Place anchor
        anchor = QPolygonF([QPointF(0, 0), QPointF(0, -ANCHOR_HEIGHT), QPointF(ANCHOR_WIDTH, -ANCHOR_HEIGHT)])

        # Place bubble rect above anchor
        self.text.adjustSize()
        rect = QRectF(QPointF(0, 0), self.text.document().size())
        rect.adjust(-MARGIN, 0, MARGIN, 2*MARGIN)

        minWidth = 2*MARGIN + ANCHOR_WIDTH
        if rect.width() < minWidth:
            rect.setWidth(minWidth)
        rect.translate(0, -rect.height() - ANCHOR_HEIGHT)

        # Position text in bubble rect
        self.text.setPos(rect.left() + MARGIN, rect.top() + MARGIN)

        # Avoid blurry borders
        anchor.translate(0.5, 0.5)
        rect.translate(0.5, 0.5)

        path = QPainterPath()
        path.addRect(rect)
        path.addPolygon(anchor)
        self.setPath(path.simplified())


class AddBubbleTool(SceneTool):
    def mousePressEvent(self, event):
        item = self.scene.itemAt(event.scenePos())
        if isinstance(item, Bubble):
            return False

        bubble = Bubble()
        self.scene.addItem(bubble)
        bubble.setPos(event.scenePos())
        bubble.text.setFocus()
        return True
# vi: ts=4 sw=4 et
