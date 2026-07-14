from rubicon.objc import ObjCClass, SEL, objc_method, objc_property
from travertino.size import at_least

try:
    from toga_iOS.widgets.base import Widget
except ImportError:
    class Widget:
        def __init__(self, interface):
            self.interface = interface
            self._container = None
            self.native = None
            self.create()

        def set_app(self, app):
            pass

        def set_window(self, window):
            pass

        def set_bounds(self, x, y, width, height):
            if hasattr(self, 'constraints') and self.constraints:
                self.constraints.update(x, y, width, height)

        def add_constraints(self):
            pass

        def rehint(self):
            pass


UIButton = ObjCClass('UIButton')


class TogaButton(UIButton):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def onPress_(self, sender):
        self.interface.on_press()


class TaButtonImpl(Widget):
    focusable = False

    def create(self):
        self.native = TogaButton.buttonWithType(0)
        self.native.interface = self.interface
        self.native.impl = self
        self.native.addTarget_action_forControlEvents(
            self.native, SEL("onPress:"), 1 << 6
        )
        self._icon = None

    def get_text(self):
        return str(self.native.titleForState(0)) or ''

    def set_text(self, text):
        self.native.setTitle_forState(text or '', 0)

    def get_icon(self):
        return self._icon

    def set_icon(self, icon, size=-1):
        self._icon = icon
        if icon:
            drawable = icon._impl.as_drawable(self, size)
            self.native.setImage_forState(drawable, 0)
        else:
            self.native.setImage_forState(None, 0)

    def set_enabled(self, value):
        self.native.setEnabled(value)

    def set_background_color(self, value):
        if value:
            UIColor = ObjCClass('UIColor')
            color = UIColor.colorWithRed_green_blue_alpha_(
                value.red, value.green, value.blue, value.alpha
            )
            self.native.setBackgroundColor(color)

    def rehint(self):
        self.native.sizeToFit()
        self.interface.intrinsic.width = at_least(self.native.frame.size.width)
        self.interface.intrinsic.height = self.native.frame.size.height
