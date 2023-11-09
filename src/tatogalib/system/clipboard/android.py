from android.content import ClipboardManager, ClipData
import java
import toga


class ClipboardImpl:
    clipboard_manager = None
    data_types = ("Text", "URI", "Intent")

    def __init__(self, interface):
        self.interface = interface
        self.context = toga.App.app._impl.native
        clipboard = self.context.getSystemService(
            "clipboard"
        )  # returns a java/lang/Object
        # cast the Object to ClipboardManager and assign it to self.clipboard_manager
        self.clipboard_manager = java.cast(ClipboardManager, clipboard)

    # __init__

    def clear(self):
        self.clipboard_manager.clearPrimaryClip()

    # clear

    def get_text(self):
        if self.clipboard_manager.hasPrimaryClip():
            clip_data = self.clipboard_manager.getPrimaryClip()
            item = clip_data.getItemAt(0)
            if item.getText():
                return item.getText()
            else:
                return None
        else:
            return None

    # get_text

    def set_text(self, text):
        if text is None:
            self.clear()
        else:
            clip_data = ClipData.newPlainText(self.data_types[0], text)
            self.clipboard_manager.setPrimaryClip(clip_data)

    # set_text


# ClipboardImpl


version = "0.5.0"
version_date = "2023-06-19 - 2023-06-19"
