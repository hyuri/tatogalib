"""
window
======

Module with several handy Python window classes for the toga framework

  Copyright (c) 2020 Tom Arn, www.tanapro.ch

For suggestions and questions:
<sw@tanapro.ch>

This file is distributed under the terms of the MIT license
"""

import copy
from threading import Timer
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from .. import system


class TaGui:
    """
    Template class for new GUIs. In the constructor, you can use all keyword arguments from Window or MainWindow
    Derived classes must call super().__init__() and implement the method build_gui()
    build_gui() must return a Widget (typically a Box or a container) which contains all content of the GUI.
    Then, the window can be shown by calling the show() method of the class

    Example code (works the same for the main GUI and sub GUIs)::

        # in app.py:
        mygui = user_gui.MainGui(
            self, None, "Main GUI", size=(600, 480)  # using None for the parentGui marks the main gui
        )
        mygui.show()

        # in user_gui:
        class MainGui(TaGui):

            def __init__(self, app, parentGui, title, **kwargs):
                super().__init__(app, parentGui, title, **kwargs)
            # __init__

            def build_gui(self) -> toga.Widget:
                # create box for content
                top_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
                top_box.add(toga.Label("Hello"))

                # button bar
                button_box = toga.Box(style=Pack(direction=ROW, padding=(5, 0, 0, 0)))  # top, right, bottom and left padding
                button_box.add(toga.Label("", style=Pack(flex=1)))
                button_box.add(toga.Button("OK", on_press=self.handle_OK_button))
                button_box.add(toga.Label("", style=Pack(flex=1)))
                top_box.add(button_box)
                return top_box
            # build_gui

    Currently supported platforms: windows, android, iOS

    """

    def __init__(self, app, parentGui, title, **kwargs):
        """
        Creates a new GUI class

        :param toga.App app: The app object
        :param TaGui parentGui: The parent GUI of this GUI - must inherit from TaGui - Use None for the main window
        :param str title: The title of the window to be created
        :param kwargs: All keyword arguments allowed in MainWindow or TaWindow
        """
        self.root_box = None
        self.window = None
        self.app = app
        self.parentGui = parentGui
        self.title = title
        self.parent_commands = None
        self.parent_toolbar = None
        if parentGui is not None and not isinstance(parentGui, TaGui):
            print("Type of parentGui: {}".format(str(type(parentGui))))
            raise TypeError("parentGui must inherit from TaGui!")
        # create the window
        if parentGui is None:  # main GUI
            self.app.main_window = toga.MainWindow(title=title, **kwargs)
            self.window = self.app.main_window
        else:  # sub GUIs
            current_platform = system.get_platform()
            if current_platform == "Windows":
                self.window = TaWindow(self.parentGui.window, title, **kwargs)
            elif current_platform in ("Android", "iOS"):
                self.window = self.parentGui.window
            else:
                raise NotImplementedError(
                    f"TaGui: unsupported platform {current_platform}"
                )
            if current_platform in ("Android", "iOS"):
                # save parent commands and toolbar
                self.parent_commands = copy.copy(self.app.commands)
                self.parent_toolbar = copy.copy(self.app.main_window.toolbar)

    # __init__

    def build_gui(self) -> toga.Widget:
        """
        This method must be implemented by the derived class to create the user GUI

        :returns: The root Widget which contains all of the user GUI elements
        :rtype: Typically a Box or some container
        """
        raise NotImplementedError(
            "TaGui: You must implement build_gui() -> Widget in your derived class!"
        )

    # build_gui

    def close(self):
        """
        Closes the current GUI.
        On Android and iOS, it calls parentGui.show() to restore the previous GUI
        """
        current_platform = system.get_platform()
        if current_platform == "Windows":
            self.window.close()
        # restore parent commands and toolbar
        if plat == "Android":
            self.app._commands = self.parent_commands
            self.app.main_window._toolbar = self.parent_toolbar
            self.app._impl.native.invalidateOptionsMenu()
            self.parentGui.show()
        elif current_platform == "iOS":
            self.app._commands = self.parent_commands
            self.app.main_window._toolbar = self.parent_toolbar
            self.parentGui.show()

    # close

    def get_scale(self):
        """
        Returns the scale factor of the platform.
        Multiply dp values with this factor to get px values.

        :returns: The scale factor
        :rtype: float
        """
        return self.window.content._impl.dpi_scale

    # get_scale

    def get_window_size(self):
        """
        Returns the usable (width, height) of this window in dp

        :returns: The size of the current window
        :rtype: (int, int)
        """
        return self.window.size

    # get_window_size

    def show(self):
        """
        Calls build_gui() and displays the GUI.
        Override build_gui() method in derived classes to implement the user GUI
        """
        if self.root_box is None:
            print("Calling build_gui()")
            self.root_box = self.build_gui()
        if self.root_box is None:
            raise NotImplementedError(
                "TaGui: You must implement build_gui() -> Widget in your derived class!"
            )
        self.window.content = self.root_box
        # setting app title
        current_platform = system.get_platform()
        if current_platform == "Android":
            self.app._impl.native.setTitle(self.title)
        elif current_platform == "iOS":
            self.app.main_window.native.navigationItem.title = self.title
        self.window.show()

    # show


# TaGui


class TaWindow(toga.Window):
    """
    Extension of toga.Window with following features:
    - auto closeable
    - auto centered on parent window

    This class is only supported on windows.
    """

    def __init__(
        self,
        parentWindow,
        title,
        size=(200, 200),
        position=None,
        auto_close_duration=None,
        on_close=None,
    ):
        """
        Creates a new TaWindow.

        :param toga.Window parentWindow: The toga.Window which is the parent of this TaWindow
        :param str title: The title for this window
        :param tuple[int, int] size: The initial size (width, height) in dp of this HtmlWindow
        :param position: The initial position (x, y) of this HtmlWindow. None centers it on parentWindow
        :type position: tuple[int, int] or None
        :param auto_close_duration: The time in seconds after which this HtmlWindow closes automatically
        :type auto_close_duration: float or None
        :param on_close: The callable that will be called when the user closes the window
        """
        self._timer = None
        self.parentWindow = parentWindow
        self._centerOnParent = False
        self._auto_close_duration = auto_close_duration
        self._user_on_close = on_close
        if position is None:
            position = (100, 100)
            self._centerOnParent = True
        super().__init__(title=title, size=size, position=position)

    # __init__

    def close(self):
        """
        Cancels a possibly active auto-close timer and closes the window
        """
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None
        super().close()

    # close

    def window_close_handler(self, window):
        """
        Cancels a possibly active auto-close timer when the window should close

        :returns: True when the window should close, False when it should stay open
        :rtype: bool
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

    # window_close_handler

    def show(self):
        """
        Shows the window
        """
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


class HtmlWindow(TaWindow):
    """
    Class which shows a TaWindow with html content.
    If no position is passed, the window will center on its parent

    This class is only supported on windows.
    """

    def __init__(
        self,
        parentWindow,
        title,
        html_text,
        size=(200, 200),
        font_size=None,
        position=None,
        auto_close_duration=None,
        on_close=None,
    ):
        """
        Creates a window with a WebView.

        :param toga.Window parentWindow: The toga.Window which is the parent of this HtmlWindow
        :param str title: The title for this window
        :param size: The initial size (width, height) in dip of this HtmlWindow
        :type size: tuple[(int, int)]
        :param str html_text: The html text to display
        :param position: The initial position (x, y) of this HtmlWindow. None centers it on parentWindow
        :type position: tuple[(int, int)] or None
        :param auto_close_duration: The time in seconds after which this HtmlWindow closes automatically
        :type auto_close_duration: float or None
        :param on_close: The callable that will be called when the user closes the window
        """
        self.font_size = font_size
        super().__init__(
            parentWindow,
            title,
            size=size,
            position=position,
            auto_close_duration=auto_close_duration,
            on_close=on_close,
        )
        self._mainBox = toga.Box(style=Pack(direction=COLUMN, padding=5, flex=1))
        self.webView = toga.WebView(style=Pack(flex=1))
        self.webView.set_content("data:text/html,", html_text)
        self._mainBox.add(self.webView)

    # __init__

    def add_ok_button(self):
        """Adds an OK button at the bottom."""
        button_box = toga.Box(
            style=Pack(direction=ROW, padding=(5, 0, 0, 0))
        )  # top, right, bottom and left padding
        button_box.add(toga.Label("", style=Pack(flex=1)))
        if self.font_size is None:
            button_box.add(toga.Button("OK", on_press=self.handle_ok_button))
        else:
            button_box.add(
                toga.Button(
                    "OK",
                    on_press=self.handle_ok_button,
                    style=Pack(font_size=self.font_size),
                )
            )
        button_box.add(toga.Label("", style=Pack(flex=1)))
        self._mainBox.add(button_box)

    # add_ok_button

    def handle_ok_button(self, widget):
        self.close()

    # handle_ok_button

    def show(self):
        self.content = self._mainBox
        super().show()

    # show


# HtmlWindow


def centerOnParent(parent_window, child_window):
    if parent_window is not None:
        _location = parent_window.position
        _parentSize = parent_window.size
        _x = int(_location[0] + (_parentSize[0] - child_window.size[0]) / 2)
        _y = int(_location[1] + (_parentSize[1] - child_window.size[1]) / 2)
        child_window.position = (_x, _y)


# centerOnParent


version = "0.9.6"
version_date = "2020-08-10 - 2023-11-07"
