#!/usr/bin/env python
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PyKDE4.kdecore import *
from PyKDE4.kdeui import *

from controller import Controller


def main():
    KCmdLineArgs.init(sys.argv, \
        "annot8", \
        "", \
        ki18n("Annot8"), \
        "1.0", \
        ki18n("Screenshot annotation tool"))

    options = KCmdLineOptions()
    KCmdLineArgs.addCmdLineOptions(options)

    app = KApplication()
    controller = Controller()

    controller.show()
    if len(sys.argv) == 2:
        controller.load(sys.argv[1])
    app.exec_()
    return 0


if __name__=="__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
