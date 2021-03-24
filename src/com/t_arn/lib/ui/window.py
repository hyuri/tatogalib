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

    def __init__(self, parentWindow, title, size=(200, 200), position=None, auto_close_duration=None):
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
        """
        self.parentWindow = parentWindow
        self._centerOnParent = False
        self._auto_close_duration = auto_close_duration
        if position is None:
            position = (100, 100)
            self._centerOnParent = True
        super().__init__(title=title, size=size, position=position)
    # __init__

    def close(self):
        """Cancels a possibly active auto-close timer and closes the window"""
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None
        super().close()
    # close

    def on_close(self):
        """Cancels a possibly active auto-close timer and calls its super method"""
        # todo: on_close not implemented in winforms
        if self._timer is not None:
            print('cancel timer (on_close)')
            self._timer.cancel()
            self._timer = None
        print('super().on_close()')
        super().on_close()

    def show(self):
        if self._centerOnParent is True:
            centerOnParent(self.parentWindow, self)
        if self._auto_close_duration is not None:
            self._timer = Timer(self._auto_close_duration, self.close)
            self._timer.start()
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

    def __init__(self, parentWindow, title, html_text, size=(200, 200), position=None, auto_close_duration=None):
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
        """
        super().__init__(parentWindow, title, size, position, auto_close_duration)
        self._mainBox = toga.Box(style=Pack(direction=COLUMN, padding=5))
        self.webView = toga.WebView(style=Pack(flex=1))
        self.webView.set_content('data:text/html,', html_text)
        self._mainBox.add(self.webView)
    # __init__

    def add_ok_button(self):
        """Adds an OK button at the bottom."""
        _buttonBox = toga.Box(style=Pack(direction=ROW, padding=(5, 0, 0, 0)))  # top, right, bottom and left padding
        _buttonBox.add(toga.Label('', style=Pack(flex=1)))
        _buttonBox.add(toga.Button('OK', on_press=self.handle_ok_button))
        _buttonBox.add(toga.Label('', style=Pack(flex=1)))
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


version = '0.2'
version_date = '2020-08-10 - 2020-08-10'
