import sys
from threading import Timer
import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack
from tatogalib.ui.window import TaGui


def get_platform():
    return toga.platform.current_platform
# get_platform


class MainGui(TaGui):
    
    def __init__(self, app, parentGUI, title, **kwargs):
        self.message_area = None
        super().__init__(app, parentGUI, title, **kwargs)
    # __init__

    def create_app_commands(self):
        # do nothing because we do not want the default commands
        pass

    def build_gui(self) -> toga.Widget:
        top_box = toga.Box(style=Pack(flex=1, direction=COLUMN, padding=5))
        self.app._impl._create_app_commands = self.create_app_commands  # disable default commands
        if get_platform() == "windows":
            # adding commands
            # add actions
            grpFile = toga.Group(text="File", order=1)
            # add actions
            cmdExit = toga.Command(
                lambda s: self.app.exit(),
                text="Exit",
                group=grpFile,
                section=sys.maxsize,
            )
            self.app.commands.add(cmdExit)

            grpHelp = toga.Group(text="Help", order=3)
            cmdInfo = toga.Command(
                self.info, text="Info", group=grpHelp, order=1
            )
            self.app.commands.add(cmdInfo)
        # win32

        if get_platform() == "android":
            # Menu
            cmdInfo = toga.Command(
                self.info,
                text="Info",
                group=toga.Group.COMMANDS,
                order=10,
                section=sys.maxsize
            )
            self.app.commands.add(cmdInfo)
        mti_message = toga.MultilineTextInput(placeholder="Enter some text here...", style=Pack(flex=1))
        top_box.add(mti_message)
        if get_platform() == "windows":
            top_box.add(toga.Button("Auto-closing window", on_press=self.auto_closing_window))
        return top_box
    # build_gui

    def info(self, widget):
        html_text = "<h1>Info</h1><p>This is a test application for the tatogalib.ui.window module</p>"
        gui = WebViewGui(self.app, self, "Info window", html_text)
        gui.show()
    # info

    def auto_closing_window(self, widget):
        gui = AutoClosingGui(self.app, self, "Auto-Closing Window", auto_close_duration=5.5)
        gui.show()
    # auto_closing_window

# MainGui


class AutoClosingGui(TaGui):

    def __init__(self, app, parentGui, title, ok_button=True, **kwargs):
        self.auto_close_duration = None
        if "size" not in kwargs or (kwargs["size"] is None):
            kwargs["size"] = (int(parentGui.window.size[0]*0.8), int(parentGui.window.size[1]*0.8))
        if "position" not in kwargs or (kwargs["position"] is None):
            kwargs["position"] = None
        if "auto_close_duration" in kwargs:
            self.auto_close_duration = kwargs["auto_close_duration"]
        super().__init__(app, parentGui, title, **kwargs)
        self._ok_button = ok_button
    # __init__

    def build_gui(self) -> toga.Widget:
        # create box for content
        top_box = toga.Box(style=Pack(flex=1, direction=COLUMN))
        top_box.add(toga.Label(f"This window will auto-close in {self.auto_close_duration} seconds"))
        # commands
        if get_platform() == "android":
            self.app.commands.clear()
            cmdBack = toga.Command(
                self.handle_ok_button,
                text="Back",
                group=toga.Group.COMMANDS,
                order=10,
            )
            self.app.commands.add(cmdBack)

        # button bar
        if self._ok_button is True:
            box_buttons = toga.Box(
                style=Pack(direction=ROW, padding=(5, 0, 0, 0))
            )  # top, right, bottom and left padding
            box_buttons.add(toga.Label("", style=Pack(flex=1)))
            box_buttons.add(toga.Button("OK", on_press=self.handle_ok_button))
            box_buttons.add(toga.Label("", style=Pack(flex=1)))
            top_box.add(box_buttons)
        return top_box
    # build_gui

    def handle_ok_button(self, widget):
        self.close()
    # handle_ok_button

# AutoClosingGui


class WebViewGui(TaGui):

    def __init__(self, app, parentGui, title, html_text=None, ok_button=True, **kwargs):
        self._webView = None
        if "size" not in kwargs or (kwargs["size"] is None):
            kwargs["size"] = (300, 200)
        if "position" not in kwargs or (kwargs["position"] is None):
            kwargs["position"] = None
        super().__init__(app, parentGui, title, **kwargs)
        self._html_text = html_text
        self._ok_button = ok_button
    # __init__

    def build_gui(self) -> toga.Widget:
        # create box for content
        top_box = toga.Box(style=Pack(flex=1, direction=COLUMN))
        self._webView = toga.WebView(style=Pack(flex=1))
        self._webView.set_content("", self._html_text)
        top_box.add(self._webView)

        # commands
        if get_platform() == "android":
            self.app.commands.clear()
            cmdBack = toga.Command(
                self.handle_ok_button,
                text="Back",
                group=toga.Group.COMMANDS,
                order=10,
            )
            self.app.commands.add(cmdBack)

        # button bar
        if self._ok_button is True:
            box_buttons = toga.Box(
                style=Pack(direction=ROW, padding=(5, 0, 0, 0))
            )  # top, right, bottom and left padding
            box_buttons.add(toga.Label("", style=Pack(flex=1)))
            box_buttons.add(toga.Button("OK", on_press=self.handle_ok_button))
            box_buttons.add(toga.Label("", style=Pack(flex=1)))
            top_box.add(box_buttons)
        return top_box
    # build_gui

    def handle_ok_button(self, widget):
        self.close()
    # handle_ok_button
# WebViewGui
