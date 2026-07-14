from rubicon.objc import ObjCClass, NSObject, objc_method, objc_property
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


class TogaPickerDelegate(NSObject):
    impl = objc_property(object, weak=True)

    @objc_method
    def numberOfComponentsInPickerView_(self, pickerView):
        return 1

    @objc_method
    def pickerView_numberOfRowsInComponent_(self, pickerView, component):
        return len(self.impl.interface._items)

    @objc_method
    def pickerView_titleForRow_forComponent_(self, pickerView, row, component):
        item = self.impl.interface._items[row]
        return self.impl.interface._title_for_item(item)

    @objc_method
    def pickerView_didSelectRow_inComponent_(self, pickerView, row, component):
        self.impl.on_change(row)


class TaSelectionImpl(Widget):
    focusable = False

    def create(self):
        UIPickerView = ObjCClass('UIPickerView')
        self.native = UIPickerView.alloc().init()
        self.delegate = TogaPickerDelegate.alloc().init()
        self.delegate.impl = self
        self.native.delegate = self.delegate
        self.native.dataSource = self.delegate
        self.last_selection = None

    def on_change(self, index):
        if index != self.last_selection:
            self.interface.on_change()
            self.last_selection = index

    def insert(self, index, item):
        self.native.reloadAllComponents()
        if self.last_selection is None:
            self.select_item(0)
        elif index <= self.last_selection:
            self.last_selection += 1
            self.select_item(self.last_selection)

    def change(self, item):
        self.native.reloadAllComponents()

    def remove(self, index, item=None):
        self.native.reloadAllComponents()
        removed_selection = self.last_selection == index
        if index <= self.last_selection:
            if len(self.interface._items) == 0:
                self.last_selection = None
            else:
                self.last_selection = max(0, self.last_selection - 1)
                self.select_item(self.last_selection)
        if removed_selection:
            self.interface.on_change()

    def select_item(self, index, item=None):
        self.native.selectRow_inComponent_animated(index, 0, False)
        self.on_change(index)

    def get_selected_index(self):
        selected = self.native.selectedRowInComponent(0)
        return None if selected == -1 else selected

    def clear(self):
        self.native.reloadAllComponents()
        self.on_change(None)

    def rehint(self):
        self.native.sizeToFit()
        self.interface.intrinsic.width = at_least(self.native.frame.size.width)
        self.interface.intrinsic.height = self.native.frame.size.height

    def set_font(self, font):
        pass
