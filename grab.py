import time

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PyKDE4.kdecore import *
from PyKDE4.kdeui import *

from ui_grabdialog import Ui_GrabDialog

class GrabDialog(KDialog):
    def __init__(self):
        KDialog.__init__(self)

        self.pixmap = None
        self.setupDialog()
        self.restoreConfig()

    def restoreConfig(self):
        self.ui.delaySpinBox.setValue(5)

    def setupDialog(self):
        margin = 24

        self.widget = QWidget(self)
        self.ui = Ui_GrabDialog()
        self.ui.setupUi(self.widget)
        self.setMainWidget(self.widget)
        self.widget.layout().setContentsMargins(margin, margin / 2, margin, margin)
        self.showButtonSeparator(True)
        self.setButtonText(KDialog.Ok, self.tr("Grab"))


class CountDownDialog(QDialog):
    def __init__(self, delay):
        QDialog.__init__(self)
        self.countDown = delay
        self.setupDialog()
        self.setupAnimation()

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        QObject.connect(self.timer, SIGNAL("timeout()"), self.decreaseCount)

    def exec_(self):
        self.timer.start()
        self.centerDialog()
        return QDialog.exec_(self)

    def setupDialog(self):
        self.setWindowFlags(Qt.ToolTip)
        self.setAutoFillBackground(True)
        self.setMouseTracking(True)
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor.fromRgbF(0, 0, 0, 0.8))
        pal.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(pal)

        font = self.font()
        font.setPixelSize(36)
        font.setBold(True)
        self.setFont(font)

        fm = QFontMetrics(font)
        size = fm.size(0, "8")
        extent = max(size.width(), size.height()) + 24
        self.setFixedSize(extent, extent)

    def setupAnimation(self):
        self.animation = QPropertyAnimation(self, "pos", self)
        self.animation.setDirection(QAbstractAnimation.Backward)
        self.animation.setDuration(200)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.eraseRect(self.rect())
        painter.drawText(self.rect(), Qt.AlignCenter, str(self.countDown))

    def centerDialog(self):
        screenRect = QApplication.desktop().screenGeometry()
        x = (screenRect.width() - self.width()) / 2
        y = (screenRect.height() - self.height()) / 2

        self.animation.setStartValue(QPoint(x, y))
        self.animation.setEndValue(QPoint(x + self.width(), y))
        self.move(x, y)

    def decreaseCount(self):
        self.countDown -= 1
        if self.countDown == 0:
            self.accept()
        else:
            self.update()

    def mouseMoveEvent(self, event):
        QDialog.mouseMoveEvent(self, event)
        if self.animation.state() != QAbstractAnimation.Running:
            direction = self.animation.direction()
            if direction == QAbstractAnimation.Backward:
                direction = QAbstractAnimation.Forward
            else:
                direction = QAbstractAnimation.Backward
            self.animation.setDirection(direction)
            self.animation.start()


def grabActiveWindow():
    wid = KWindowSystem.activeWindow()
    return QPixmap.grabWindow(wid)


def grabWholeScreen():
    wid = QApplication.desktop().winId()
    return QPixmap.grabWindow(wid)


def showDialog():
    dialog = GrabDialog()
    ret = dialog.exec_()
    if ret != QDialog.Accepted:
        return None

    delay = dialog.ui.delaySpinBox.value()
    wholeScreen = dialog.ui.wholeScreenButton.isChecked()

    dialog = CountDownDialog(delay)
    dialog.exec_()
    # Give enough time to the dialog to go away (important in composite mode)
    time.sleep(1)
    if wholeScreen:
        return grabWholeScreen()
    else:
        return grabActiveWindow()


# vi: ts=4 sw=4 et
