from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Handle(QGraphicsObject):
    HANDLE_RADIUS = 5
    CircleType = 1
    TopLeftType = 2
    BottomRightType = 3

    moved = pyqtSignal(QGraphicsObject)
    mousePressed = pyqtSignal(QGraphicsObject)
    mouseReleased = pyqtSignal(QGraphicsObject)

    def __init__(self, parent, x, y):
        QGraphicsObject.__init__(self, parent)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setPos(x, y)
        self._path = None
        self._handleType = None
        self.handleType = Handle.CircleType
        self.setAcceptHoverEvents(True)

        self._opacityAnimation = QPropertyAnimation(self, "opacity", self)
        minOpacity = 0.5
        self.setOpacity(minOpacity)
        self._opacityAnimation.setStartValue(minOpacity)
        self._opacityAnimation.setEndValue(1)

    @property
    def minOpacity(self):
        return self._opacityAnimation.startValue()

    @minOpacity.setter
    def minOpacity(self, value):
        self._opacityAnimation.setStartValue(value)
        # Assume we are not set while mouse is over us
        self.setOpacity(value)

    @property
    def handleType(self):
        return self._handleType

    @handleType.setter
    def handleType(self, handleType):
        self.prepareGeometryChange()

        radius = self.HANDLE_RADIUS
        self._path = QPainterPath()
        if handleType == self.CircleType:
            rect = QRectF(-radius, -radius, 2 * radius, 2 * radius)
            self._path.addEllipse(rect)

        elif handleType == self.TopLeftType:
            self._path.lineTo(radius * 2, 0)
            self._path.lineTo(0, radius * 2)
            self._path.closeSubpath()
            self._path.translate(0.5, 0.5)

        elif handleType == self.BottomRightType:
            self._path.lineTo(-radius * 2, 0)
            self._path.lineTo(0, -radius * 2)
            self._path.closeSubpath()
            self._path.translate(-0.5, -0.5)

        self.update()

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            self.moved.emit(self)
        return QGraphicsObject.itemChange(self, change, value)

    def paint(self, painter, options, widgets):
        painter.setBrush(QColor.fromHsvF(0, 0, 1., 0.8))
        painter.drawPath(self._path)

    def boundingRect(self):
        return self._path.boundingRect()

    def hoverEnterEvent(self, event):
        QGraphicsObject.hoverEnterEvent(self, event)
        self._opacityAnimation.setDirection(QAbstractAnimation.Forward)
        self._opacityAnimation.start()

    def hoverLeaveEvent(self, event):
        QGraphicsObject.hoverLeaveEvent(self, event)
        self._opacityAnimation.setDirection(QAbstractAnimation.Backward)
        self._opacityAnimation.start()

    def mousePressEvent(self, event):
        QGraphicsObject.mousePressEvent(self, event)
        self.mousePressed.emit(self)

    def mouseReleaseEvent(self, event):
        QGraphicsObject.mouseReleaseEvent(self, event)
        self.mouseReleased.emit(self)

# vi: ts=4 sw=4 et
