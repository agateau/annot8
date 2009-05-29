from PyQt4.QtCore import *
from PyQt4.QtGui import *


class ToolBar(QGraphicsWidget):
    def __init__(self, orientation):
        QGraphicsWidget.__init__(self)
        self.layout = QGraphicsLinearLayout(orientation)
        self.setLayout(self.layout)


    def addTool(self, text, callBack):
        button = QPushButton(text)
        QObject.connect(button, SIGNAL("clicked()"), callBack)

        item = QGraphicsProxyWidget()
        item.setWidget(button)
        self.layout.addItem(item)


# vi: ts=4 sw=4 et
