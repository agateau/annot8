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
        self.setupLabel()

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        QObject.connect(self.timer, SIGNAL("timeout()"), self.decreaseCount)

    def exec_(self):
        self.timer.start()
        return QDialog.exec_(self)

    def setupDialog(self):
        self.setWindowFlags(Qt.ToolTip)
        self.setAttribute(Qt.WA_TranslucentBackground)
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor.fromRgbF(0, 0, 0, 0.8))
        pal.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(pal)

    def setupLabel(self):
        self.label = QLabel(self)
        self.label.setAutoFillBackground(True)
        self.label.setAlignment(Qt.AlignCenter)
        layout = QHBoxLayout(self)
        layout.setMargin(0)
        layout.addWidget(self.label)

        font = self.label.font()
        font.setPixelSize(36)
        font.setBold(True)
        self.label.setFont(font)

        self.updateCountDownLabel()
        size = self.label.sizeHint()
        self.setFixedSize(size.width() + 24, size.height() + 24)

    def updateCountDownLabel(self):
        self.label.setText(str(self.countDown))

    def decreaseCount(self):
        self.countDown -= 1
        if self.countDown == 0:
            self.accept()
        else:
            self.updateCountDownLabel()


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
    dialog.move(0, 0)
    dialog.exec_()
    # Give enough time to the dialog to go away (important in composite mode)
    time.sleep(1)
    if wholeScreen:
        return grabWholeScreen()
    else:
        return grabActiveWindow()


# vi: ts=4 sw=4 et
