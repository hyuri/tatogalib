"""
Test application for the modules
- window
- appconfig
- i18nUtils
"""
import toga
from WindowTest import gui


class Window_Test(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        objMainGui = gui.MainGui(
            self, None, "Window Test", size=(600,480)
        )
        objMainGui.show()


def main():
    objApp = Window_Test()
    return objApp

