from shapesettings import ShapeSettings


class Shape(object):
    __slots__ = ["_settings", "_item", "_handles"]
    def __init__(self, item):
        self._item = item
        self._settings = ShapeSettings(self.settingsChanged)
        self._handles = []

    @property
    def settings(self):
        return self._settings

    @property
    def item(self):
        return self._item

    @property
    def handles(self):
        return self._handles

    def settingsChanged(self):
        pass

    def handleMoved(self, handle):
        # If this shape has been linked to a handle with a call to
        # Handle.addLinkedShape(), the handle will call this method whenever it
        # moves.
        pass

    def setHandlesVisible(self, visible):
        for handle in self._handles:
            handle.setVisible(visible)
# vi: ts=4 sw=4 et
