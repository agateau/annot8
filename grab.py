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

    def setupDialog(self):
        self.widget = QWidget(self)
        self.ui = Ui_GrabDialog()
        self.ui.setupUi(self.widget)
        self.setMainWidget(self.widget)

        self.ui.delaySpinBox.setValue(5)


class CountDownDialog(QDialog):
    def __init__(self, delay):
        QDialog.__init__(self)
        self.setWindowFlags(Qt.ToolTip)
        self.countDown = delay
        self.setupLabel()

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        QObject.connect(self.timer, SIGNAL("timeout()"), self.decreaseCount)

    def exec_(self):
        self.timer.start()
        return QDialog.exec_(self)

    def setupLabel(self):
        self.label = QLabel(self)
        layout = QHBoxLayout(self)
        layout.addWidget(self.label)

        font = self.label.font()
        font.setPixelSize(24)
        font.setBold(True)
        self.label.setFont(font)

        self.updateCountDownLabel()
        self.label.adjustSize()

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


def showDialog():
    dialog = GrabDialog()
    ret = dialog.exec_()
    if ret != QDialog.Accepted:
        return None

    dialog = CountDownDialog(dialog.ui.delaySpinBox.value())
    dialog.move(0, 0)
    dialog.exec_()
    return grabActiveWindow()


# vi: ts=4 sw=4 et
