import toga


class Clipboard:
    def __init__(self, fnLog=None):
        """
        Provides access to the system clipboard.

        :param callable fnLog: The callable which is called from the log method.
            It expects a string parameter
        """
        self._fnlog = fnLog  # for logging to user code
        self._impl = None
        if toga.platform.current_platform == "android":
            from .android import ClipboardImpl
        elif toga.platform.current_platform == "windows":
            from .windows import ClipboardImpl
        else:
            raise NotImplementedError(
                f"Clipboard is not implemented for {toga.platform.current_platform}"
            )
        self._impl = ClipboardImpl(self)

    # __init__

    def clear(self):
        """
        Clears the clipboard content
        """
        self._impl.clear()

    # clear

    def get_text(self):
        """
        Get the text data currently stored in the clipboard

        :returns: The clipboard text data or None
        :rtype: str or None
        """
        return self._impl.get_text()

    # get_text

    def set_text(self, text):
        """
        Put text data into the clipboard
        :param text: The text to put into the clipboard. Use None to clear the clipboard
        """
        self._impl.set_text(text)

    # set_text

    def log(self, message):
        """
        Logs a message to the user code if fnLog was passed to the constructor

        :param str message: The message to be logged
        """
        if self._fnlog is not None:
            self._fnlog(message)

    # log


# Clipboard
