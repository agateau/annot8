from PyQt4.QtCore import *
from PyQt4.QtGui import *

MARGIN = 10

class Bubble(QGraphicsEllipseItem):
    def __init__(self, text):
        QGraphicsEllipseItem.__init__(self)
        self.setFlag(QGraphicsItem.ItemIsMovable)

        self.setBrush(QColor.fromHsvF(0, 0, 1., .6))

        self.text = QGraphicsTextItem(self)
        self.text.setTextInteractionFlags(Qt.TextEditorInteraction)
        QObject.connect(self.text.document(), SIGNAL("contentsChanged()"), \
            self.adjustSizeFromText)
        self.text.setPlainText(text)

    def adjustSizeFromText(self):
        self.text.adjustSize()
        rect = QRectF(QPointF(0, 0), self.text.document().size())
        rect.adjust(-MARGIN, -MARGIN, MARGIN, MARGIN)
        self.setRect(rect)

# vi: ts=4 sw=4 et
