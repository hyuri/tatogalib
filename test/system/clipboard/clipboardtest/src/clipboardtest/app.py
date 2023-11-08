"""
Application to test the clipboard package
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from tatogalib.system.clipboard import Clipboard


class ClipboardTest(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.cb = Clipboard()
        self.mti_message = toga.MultilineTextInput(style=Pack(flex=1))
        main_box = toga.Box(style=Pack(flex=1, direction=COLUMN, padding=5))

        main_box.add(self.mti_message)
        main_box.add(toga.Button("copy", on_press=self.copy))
        main_box.add(toga.Button("paste", on_press=self.paste))
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def copy(self, widget):
        print("Copying text from MultilineTextInput to clipboard")
        self.cb.set_text(self.mti_message.value)

    def paste(self, widget):
        print("Pasting text from clipboard to MultilineTextInput")
        self.mti_message.value = self.cb.get_text()

def main():
    return ClipboardTest()
