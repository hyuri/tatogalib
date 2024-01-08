import clr
clr.AddReference("System.Windows.Forms")
import System.Windows.Forms as WinForms


class ClipboardImpl:
    def __init__(self, interface):
        self.interface = interface

    # __init__

    def clear(self):
        WinForms.Clipboard.Clear()

    # clear

    def get_text(self):
        if WinForms.Clipboard.ContainsText():
            return WinForms.Clipboard.GetText()
        else:
            return None

    # get_text

    def set_text(self, text):
        if text is None:
            self.clear()
        else:
            WinForms.Clipboard.SetText(text)

    # set_text


# ClipboardImpl


version = "0.6.0"
version_date = "2023-06-19 - 2024-01-08"
