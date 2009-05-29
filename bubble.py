from PyQt4.QtCore import *
from PyQt4.QtGui import *

OPACITY = 0.8
MARGIN = 10.5

class Bubble(QGraphicsPathItem):
    def __init__(self, text):
        QGraphicsPathItem.__init__(self)
        self.setFlag(QGraphicsItem.ItemIsMovable)

        self.setBrush(QColor.fromHsvF(0, 0, 1., OPACITY))

        self.text = QGraphicsTextItem(self)
        self.text.setTextInteractionFlags(Qt.TextEditorInteraction)
        QObject.connect(self.text.document(), SIGNAL("contentsChanged()"), \
            self.adjustSizeFromText)
        self.text.setPlainText(text)

    def adjustSizeFromText(self):
        self.text.adjustSize()
        rect = QRectF(QPointF(0, 0), self.text.document().size())
        rect.adjust(-MARGIN, -MARGIN, MARGIN, MARGIN)
        path = QPainterPath()
        path.addRect(rect)

        x = rect.left() + 5
        y = rect.bottom()
        anchor = QPolygonF([QPointF(x, y), QPointF(x, y + 20), QPointF(x + 20, y)])

        path.addPolygon(anchor)
        self.setPath(path.simplified())

# vi: ts=4 sw=4 et
