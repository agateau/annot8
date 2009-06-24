from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PyKDE4.kdecore import *
from PyKDE4.kdeui import *

def grabActiveWindow():
    wid = KWindowSystem.activeWindow()
    return QPixmap.grabWindow(wid)

# vi: ts=4 sw=4 et
