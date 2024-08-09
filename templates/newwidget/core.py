# from .base import Widget
from toga import Widget

from ... import system


if system.get_platform() == "android":
    from .android import NewWidgetImpl
elif system.get_platform() == "windows":
    from .windows import NewWidgetImpl
else:
    raise NotImplementedError(f"NewWidget is not implemented for {system.get_platform()}")


#class OriginalClass(Widget):
class NewWidget(Widget):
    def __init__(
        self,
        id,
        style,
        # other params
    ):
    """Class documentation
    """
    super().__init__(id=id, style=style)
    # self._impl = self.factory.OriginalClass(interface=self)
    self._impl = NewWidgetImpl(interface=self)
 