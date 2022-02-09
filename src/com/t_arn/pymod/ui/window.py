"""
window
======

Module with several handy Python window classes for the toga module

Copyright (c) 2020 Tom Arn, www.t-arn.com

For suggestions and questions:
<sw@t-arn.com>

This file is distributed under the terms of the LGPL
"""

from threading import Timer
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class TaGui:
    """
    Template class for new GUIs. In the constructor, you can use all keyword arguments from Window or MainWindow
    Derived classes must call super().__init__() and implement the method build_gui()
    build_gui() must create the main_box and add all content there.
    Then, the window can be shown by calling the show() method of the class

    Example code (works the same for the main GUI and sub GUIs):
    # in app.py:
    mygui = user_gui.MainGui(
        self, None, "Main GUI", size=(600, 480)  # using None for the parentGui marks the main gui
    )
    mygui.show()

    # in user_gui:
    class MainGui(TaGui):
        main_box = None

        def __init__(self, app, parentGui, title, **kwargs):
            super().__init__(app, parentGui, title, **kwargs)
        # __init__

        def build_gui(self):
            # create box for content
            self.main_box = toga.Box(style=Pack(direction=COLUMN))
            self.main_box.add(toga.Label("Hello"))

            # button bar
            box_buttons = toga.Box(style=Pack(direction=ROW, padding=(5, 0, 0, 0)))  # top, right, bottom and left padding
            box_buttons.add(toga.Label("", style=Pack(flex=1)))
            box_buttons.add(toga.Button("OK", on_press=self.handle_OK_button))
            box_buttons.add(toga.Label("", style=Pack(flex=1)))
            self.main_box.add(box_buttons)
        # build_gui
    """
    app = None
    root_box = None
    window = None
    parentGui = None
    title = None

    def __init__(self, app, parentGui, title, **kwargs):
        """
        Creates a new GUI class

        :param toga.App app: The app object
        :param TaGui parentGui: The parent GUI of this GUI - must inherit from TaGui - Use None for the main window
        :param str title: The title of the window to be created
        :param kwargs: All keyword arguments allowed in Window or MainWindow
        """
        self.app = app
        self.parentGui = parentGui
        self.title = title
        if parentGui is not None and not isinstance(parentGui, TaGui):
            print("Type of parentGui: {}".format(str(type(parentGui))))
            raise Exception("parentGui must inherit from TaGui!")
        # create the window
        if parentGui is None:  # main GUI
            self.app.main_window = toga.MainWindow(title=title, **kwargs)
            self.window = self.app.main_window
        else:  # sub GUIs
            self.window = TaWindow(self.parentGui.window, title, **kwargs)
            if toga.platform.current_platform in ("win32", "darwin"):
                self.app.windows.add(self.window)
            else:
                self.window = self.parentGui.window
        # create root_box on mobile platforms
        if toga.platform.current_platform in ("android", "ios"):
            if parentGui is None:
                self.root_box = toga.Box(style=Pack(direction=COLUMN))
            else:
                self.root_box = parentGui.root_box
    # __init__

    def close(self):
        """
        Closes the current GUI.
        On Android an iOS, calls parentGui.show() to restore the previous GUI
        """
        if toga.platform.current_platform in ("win32", "darwin"):
            self.window.close()
        if toga.platform.current_platform in ("android", "ios"):
            self.parentGui.show()
    # close

    def show(self):
        """
        Calls build_gui() and displays the GUI.
        Override build_gui() method in derived classes to implement the GUI
        """
        if self.main_box is None:
            self.build_gui()
        if toga.platform.current_platform in ("win32", "darwin"):
            self.window.content = self.main_box
            self.window.show()
        if toga.platform.current_platform in ("android", "ios"):
            if self.parentGui is None:  # main GUI
                if not self.window.content:
                    self.window.content = self.root_box
            for child in self.root_box.children:
                self.root_box.remove(child)
            self.root_box.add(self.main_box)
            # setting app title
            if toga.platform.current_platform == "android":
                self.app._impl.native.setTitle(self.title)
            self.window.show()
    # show

# TaGui


class TaWindow(toga.Window):
    """
    Extension of toga.Window with following features:
    - auto closeable
    - auto centered on parent window
    """
    parentWindow = None
    _timer = None
    _centerOnParent = False
    _auto_close_duration = None
    _user_on_close = None

    def __init__(self, parentWindow, title, size=(200, 200), position=None, auto_close_duration=None, on_close=None):
        """
        Creates a new taWindow.

        :param toga.Window parentWindow: The toga.Window which is the parent of this TaWindow
        :param str title: The title for this window
        :param size: The initial size (width, height) in pixel of this HtmlWindow
        :type size: tuple[(int, int)]
        :param position: The initial position (x, y) of this HtmlWindow. None centers it on parentWindow
        :type position: tuple[(int, int)] or None
        :param auto_close_duration: The time in seconds after which this HtmlWindow closes automatically
        :type auto_close_duration: float or None
        :param on_close: The callable that will be called when the user closes the window
        """
        self.parentWindow = parentWindow
        self._centerOnParent = False
        self._auto_close_duration = auto_close_duration
        self._user_on_close = on_close
        if position is None:
            position = (100, 100)
            self._centerOnParent = True
        super().__init__(title=title, size=size, position=position)
    # __init__

    def activate(self):
        if toga.platform.current_platform == "win32":
            self._impl.native.Activate()
    # activate

    def close(self):
        """Cancels a possibly active auto-close timer and closes the window"""
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None
        super().close()
    # close

    def window_close_handler(self, window):
        """
        Cancels a possibly active auto-close timer when the window should close
        Returns True when the window should close, False when it should stay open
        """
        _should_close = True
        if self._user_on_close is not None:
            _should_close = self._user_on_close(window)
        if _should_close:
            if self._timer is not None:
                print("cancel timer (on_close)")
                self._timer.cancel()
                self._timer = None
        return _should_close

    def show(self):
        if self._centerOnParent is True:
            centerOnParent(self.parentWindow, self)
        if self._auto_close_duration is not None:
            self._timer = Timer(self._auto_close_duration, self.close)
            self._timer.start()
        if self._auto_close_duration is not None or self._user_on_close is not None:
            self.on_close = self.window_close_handler
        super().show()
    # show

# TaWindow


class HtmlWindow (TaWindow):
    """
    Class which shows a taWindow with html content.
    If no position is passed, the window will center on its parent
    """
    webView = None
    _mainBox = None

    def __init__(self, parentWindow, title, html_text, size=(200, 200), position=None, auto_close_duration=None,
                 on_close=None):
        """
        Creates a window with a WebView.

        :param toga.Window parentWindow: The toga.Window which is the parent of this HtmlWindow
        :param str title: The title for this window
        :param size: The initial size (width, height) in pixel of this HtmlWindow
        :type size: tuple[(int, int)]
        :param str html_text: The html text to display
        :param position: The initial position (x, y) of this HtmlWindow. None centers it on parentWindow
        :type position: tuple[(int, int)] or None
        :param auto_close_duration: The time in seconds after which this HtmlWindow closes automatically
        :type auto_close_duration: float or None
        :param on_close: The callable that will be called when the user closes the window
        """
        super().__init__(parentWindow, title, size=size, position=position, auto_close_duration=auto_close_duration,
                         on_close=on_close)
        self._mainBox = toga.Box(style=Pack(direction=COLUMN, padding=5))
        self.webView = toga.WebView(style=Pack(flex=1))
        self.webView.set_content("data:text/html,", html_text)
        self._mainBox.add(self.webView)
    # __init__

    def add_ok_button(self):
        """Adds an OK button at the bottom."""
        _buttonBox = toga.Box(style=Pack(direction=ROW, padding=(5, 0, 0, 0)))  # top, right, bottom and left padding
        _buttonBox.add(toga.Label("", style=Pack(flex=1)))
        _buttonBox.add(toga.Button("OK", on_press=self.handle_ok_button))
        _buttonBox.add(toga.Label("", style=Pack(flex=1)))
        self._mainBox.add(_buttonBox)
    # add_ok_button

    def handle_ok_button(self, widget):
        self.close()
    # handle_ok_button

    def show(self):
        self.content = self._mainBox
        super().show()
    # show

# HtmlWindow


class HtmlMessageBox(HtmlWindow):
    """
    Class which displays a modal HtmlWindow
    """
    # todo: implement modal behavior

    def __init__(self, parentWindow, title, html_text, size=(200, 200)):
        super().__init__(parentWindow, title, html_text, size)
        self.add_ok_button()
    # __init__

# HtmlMessageBox


def centerOnParent(parent_window, child_window):
    if parent_window is not None:
        _location = parent_window.position
        _parentSize = parent_window.size
        _x = int(_location[0] + (_parentSize[0] - child_window.size[0]) / 2)
        _y = int(_location[1] + (_parentSize[1] - child_window.size[1]) / 2)
        child_window.position = (_x, _y)
# centerOnParent


version = "0.7.2"
version_date = "2020-08-10 - 2022-02-09"
