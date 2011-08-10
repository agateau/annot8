from PyQt4.QtCore import *
from PyQt4.QtGui import *

from handle import Handle

class PixmapItem(QGraphicsObject):
    def __init__(self):
        QGraphicsObject.__init__(self)
        self._pixmap = None
        self._cropRect = QRectF()
        self._cropOpacity = 0
        self._cropOpacityAnimation = QPropertyAnimation(self, "cropOpacity", self)
        QObject.connect(self._cropOpacityAnimation, SIGNAL("finished()"), self.slotCropOpacityAnimationFinished)
        self._cropOpacityAnimation.setStartValue(0)
        self._cropOpacityAnimation.setEndValue(0.4)

        self._topLeftHandle = self._createHandle()
        self._bottomRightHandle = self._createHandle()

    def setCropOpacity(self, value):
        if self._cropOpacity != value:
            self._cropOpacity = value
            self.update()

    @pyqtProperty(float, fset=setCropOpacity)
    def cropOpacity(self):
        return self._cropOpacity

    def slotCropOpacityAnimationFinished(self):
        if not self._isFullImageVisible():
            # Cropped-out part is now fully invisible, adjust geometry
            self.prepareGeometryChange()

    def _createHandle(self):
        handle = Handle(self, 0, 0)
        QObject.connect(handle, SIGNAL("moved(QGraphicsObject*)"), self.updateCropRect)
        QObject.connect(handle, SIGNAL("mousePressed(QGraphicsObject*)"), self.onMousePressedOnHandle)
        QObject.connect(handle, SIGNAL("mouseReleased(QGraphicsObject*)"), self.onMouseReleasedOnHandle)
        return handle

    def setPixmap(self, pixmap):
        self._pixmap = pixmap
        self._cropRect = QRectF(self._pixmap.rect())
        self._topLeftHandle.setPos(self._cropRect.topLeft())
        self._bottomRightHandle.setPos(self._cropRect.bottomRight())

        self._topLeftHandle.handleType = Handle.TopLeftType
        self._topLeftHandle.minOpacity = 0.2
        self._bottomRightHandle.handleType = Handle.BottomRightType
        self._bottomRightHandle.minOpacity = 0.2

    def paint(self, painter, options, widgets):
        if self._isFullImageVisible():
            painter.setOpacity(self._cropOpacity)
            painter.drawPixmap(0, 0, self._pixmap)
            painter.setOpacity(1)
        painter.drawPixmap(self._cropRect.topLeft(), self._pixmap, self._cropRect)

    def onMousePressedOnHandle(self):
        self.prepareGeometryChange()
        self._cropOpacityAnimation.setDirection(QAbstractAnimation.Forward)
        self._cropOpacityAnimation.start()

    def onMouseReleasedOnHandle(self):
        self._cropOpacityAnimation.setDirection(QAbstractAnimation.Backward)
        self._cropOpacityAnimation.start()

    def _isFullImageVisible(self):
        return self._cropOpacityAnimation.currentTime() > 0

    def boundingRect(self):
        if self._isFullImageVisible():
            return QRectF(self._pixmap.rect())
        else:
            return self._cropRect

    def updateCropRect(self):
        self.prepareGeometryChange()
        self._cropRect = QRectF(self._topLeftHandle.pos(), self._bottomRightHandle.pos())
        self.update()

    def setHandlesVisible(self, visible):
        self._topLeftHandle.setVisible(visible)
        self._bottomRightHandle.setVisible(visible)
# vi: ts=4 sw=4 et
