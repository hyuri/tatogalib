from decimal import ROUND_UP
from android.view import View
from android.widget import Button as A_Button
from java import dynamic_proxy
from travertino.size import at_least
# from .label import TextViewWidget
from toga_android.widgets.label import TextViewWidget


class TogaOnClickListener(dynamic_proxy(View.OnClickListener)):
    def __init__(self, button_impl):
        super().__init__()
        self.button_impl = button_impl

    def onClick(self, _view):
        self.button_impl.interface.on_press()


# class Button(TextViewWidget):
class TaButtonImpl(TextViewWidget):
    focusable = False

    def create(self):
        self.native = A_Button(self._native_activity)
        self.native.setOnClickListener(TogaOnClickListener(button_impl=self))
        self.cache_textview_defaults()

        self._icon = None

    def get_text(self):
        return str(self.native.getText())

    def set_text(self, text):
        self.native.setText(text)

    def get_icon(self):
        return self._icon

    def set_icon(self, icon, size=-1):
        if size == -1:
            # Scale icon to to a 48x48 CSS pixel bitmap drawable.
            size = 48
            self.interface._icon_size = size
        self._icon = icon
        if icon:
            drawable = icon._impl.as_drawable(self, size)
        else:
            drawable = None

        self.native.setCompoundDrawablesRelative(drawable, None, None, None)

    def set_enabled(self, value):
        self.native.setEnabled(value)

    def set_background_color(self, value):
        self.set_background_filter(value)

    def rehint(self):
        if self._icon:
            # Icons aren't considered "inside" the button, so they aren't part of the
            # "measured" size. Set a button size with 10px of
            # padding (in CSS pixels).
            size = self.interface._icon_size + 20
            self.interface.intrinsic.width = at_least(size)
            self.interface.intrinsic.height = size
        else:
            self.native.measure(
                View.MeasureSpec.UNSPECIFIED,
                View.MeasureSpec.UNSPECIFIED,
            )
            self.interface.intrinsic.width = self.scale_out(
                at_least(self.native.getMeasuredWidth()), ROUND_UP
            )
            self.interface.intrinsic.height = self.scale_out(
                self.native.getMeasuredHeight(), ROUND_UP
            )


version = "1.0.0"
version_date = "2024-02-20 - 2024-03-20"
