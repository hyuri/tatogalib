"""
Test application for the modules
- window
- appconfig
- i18nUtils
"""
import toga
from WindowExample import gui


class WindowExample(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        objMainGui = gui.MainGui(
            self, None, "Window Example", size=(600,480)
        )
        objMainGui.show()


def main():
    objApp = WindowExample()
    return objApp

