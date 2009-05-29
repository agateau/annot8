#!/usr/bin/env python
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *


from controller import Controller


def main():
    app = QApplication(sys.argv)
    controller = Controller()

    controller.show()
    if len(sys.argv) == 2:
        controller.load(sys.argv[1])
    app.exec_()
    return 0


if __name__=="__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
