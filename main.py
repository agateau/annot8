#!/usr/bin/env python
# encoding: utf-8
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PyKDE4.kdecore import *
from PyKDE4.kdeui import *

import grab
from controller import Controller


def createApplication():
    aboutData = KAboutData(
        "annot8", \
        "", \
        ki18n("Annot8"), \
        "1.0")
    aboutData.setLicense(KAboutData.License_GPL_V3)
    aboutData.setShortDescription(ki18n("Screenshot annotation tool"))
    aboutData.setCopyrightStatement(ki18n("(c) 2009-2011 Aurélien Gâteau"))

    KCmdLineArgs.init(sys.argv, aboutData)

    options = KCmdLineOptions()
    options.add("grab-window", ki18n("Start with a screenshot of the active window"))
    options.add("+[file]", ki18n("A starting file"))
    KCmdLineArgs.addCmdLineOptions(options)

    app = KApplication()
    return app


def main():
    app = createApplication()

    args = KCmdLineArgs.parsedArgs()
    if args.isSet("grab-window"):
        pixmap = grab.grabActiveWindow()
    else:
        pixmap = None

    controller = Controller()
    controller.show()
    if pixmap:
        controller.setPixmap(pixmap)
    elif args.count() > 0:
        url = args.url(0)
        controller.load(url.path())
    app.exec_()
    return 0


if __name__=="__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
