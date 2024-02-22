from decimal import ROUND_UP
import clr
clr.AddReference("System.Windows.Forms")
import System.Windows.Forms as WinForms
from System.Drawing import Bitmap, Size
from travertino.size import at_least
# from ..libs.wrapper import WeakrefCallable
from toga_winforms.libs.wrapper import WeakrefCallable
# from .base import Widget
from toga_winforms.widgets.base import Widget


# class Button(Widget):
class TaButtonImpl(Widget):
    _background_supports_alpha = False

    def create(self):
        self.native = WinForms.Button()
        self.native.AutoSizeMode = WinForms.AutoSizeMode.GrowAndShrink
        self.native.Click += WeakrefCallable(self.winforms_click)

        self._icon = None

    def winforms_click(self, sender, event):
        self.interface.on_press()

    def get_text(self):
        value = self.native.Text
        # Normalize a standalone ZERO WIDTH SPACE to an empty string.
        if value == "\u200B":
            return ""
        return value

    def set_text(self, text):
        if text == "":
            # An empty label would cause the widget's height to collapse, so display a
            # Unicode ZERO WIDTH SPACE instead.
            text = "\u200B"
        self.native.Text = text

    def get_icon(self):
        return self._icon

    def set_icon(self, icon, size=-1):
        if size == -1:
            # Scale icon to to a 32x32 CSS pixel bitmap.
            size = 32
            self.interface._icon_size = size
        self._icon = icon
        if icon:
            bitmap = icon._impl.native.ToBitmap()
            native_size = Size(self.scale_in(size), self.scale_in(size))
            self.native.Image = Bitmap(bitmap, native_size)
        else:
            self.native.Image = None

    def rehint(self):
        self.interface.intrinsic.width = self.scale_out(
            at_least(self.native.PreferredSize.Width), ROUND_UP
        )
        self.interface.intrinsic.height = self.scale_out(
            self.native.PreferredSize.Height, ROUND_UP
        )

version = "1.0.0"
version_date = "2024-02-20 - 2024-03-20"
