from shapesettings import ShapeSettings


class Shape(object):
    __slots__ = ["_settings", "_item"]
    def __init__(self, item):
        self._item = item
        self._settings = ShapeSettings(self.settingsChanged)

    @property
    def settings(self):
        return self._settings

    @property
    def item(self):
        return self._item

    def settingsChanged(self):
        pass
# vi: ts=4 sw=4 et
