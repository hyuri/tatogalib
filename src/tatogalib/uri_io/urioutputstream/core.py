import os

from ... import system


class UriOutputStream:
    def __init__(self, uristring, mode, fnLog=None):
        """
        Creates a UriOutputStream which wraps a RawIOBase stream.
        This class supports the context manager protocol.

        :param str uristring: The URI-string of the stream
        :param str mode: "wb" for overwriting, "ab" for appending
        :param callable fnLog: The callable which is called from the log method
            It expects a string parameter
        """
        self.uristring = uristring
        self.mode = mode
        if mode != "wb" and mode != "ab":
            raise ValueError(
                f'UriOutputStream: Invalid mode "{mode}"! Valid modes are "wb" or "ab"'
            )
        self._fnlog = fnLog  # for logging to user code
        plat = system.get_platform()
        if plat == "Android":
            from .android import UriOutputStreamImpl
        elif plat == "iOS":
            from .ios import UriOutputStreamImpl
        elif plat in ("Windows", "Linux", "Darwin"):
            from .desktop import UriOutputStreamImpl
        else:
            raise NotImplementedError(
                f"UriOutputStream is not implemented for {plat}"
            )
        self._impl = UriOutputStreamImpl(self, mode)

    # __init__

    def __enter__(self):
        return self

    # __enter

    def __exit__(self, exc_type, exc_value, traceback):
        if self._impl is not None:
            try:
                self.close()
            except BaseException as ex:
                pass
        return False  # propagate exceptions

    # __exit__

    def close(self):
        """
        Flushes and closes the stream
        """
        self.flush()
        self._impl.close()

    # close

    @property
    def closed(self):
        """
        Checks if the stream is closed

        :returns: True when closed, False otherwise
        """
        return self._impl.closed()

    # closed

    def read(self, maxsize=-1):
        """
        This method will raise an OS error when it is called
        """
        raise OSError(22, "not readable")

    # read

    def readinto(self, bytesobj):
        """
        This method will raise an OS error when it is called
        """
        raise OSError(22, "not readable")

    # readinto

    def readall(self):
        """
        This method will raise an OS error when it is called
        """
        raise OSError(22, "not readable")

    # readall

    def readable(self):
        """
        This method always returns False

        :returns: False
        """
        return False

    # readable

    def write(self, bytesobj):
        """
        Writes bytes to the stream

        :param bytes bytesobj: The bytes to be written

        :returns: The amount of bytes written
        :rtype: int
        """
        return self._impl.write(bytesobj)

    # write

    def flush(self):
        """
        Flushes the write buffer of stream if applicable
        """
        self._impl.flush()

    # flush

    def isatty(self):
        """
        This method always returns False

        :returns: False
        """
        return False

    # isatty

    def seekable(self):
        """
        Checks if the stream is seekable

        :returns: True when seekable, False otherwise
        """
        return self._impl.seekable()

    # seekable

    def truncate(self, size=None):
        """
        Resizes the stream to the given size.
        This is currently unimplemented on Android

        :param int size: The new size in bytes

        :returns: The new size in bytes
        :rtype: int
        """
        return self._impl.truncate(size)

    # truncate

    def writable(self):
        """
        Checks if the stream is writable

        :returns: True when writable, False otherwise
        """
        return self._impl.writable()

    # writable

    def log(self, message):
        """
        Logs a message to the user code if fnLog was passed to the constructor

        :param str message: The message to be logged
        """
        if self._fnlog is not None:
            self._fnlog(message)

    # log


# UriOutputStream


class UriTextOutputStream:
    def __init__(self, uristring, mode, encoding, newline=None, fnLog=None):
        """
        Creates a UriTextOutputStream which wraps a UriOutputStream.
        This class supports the context manager protocol.

        :param str uristring: The URI-string of the stream
        :param str mode: "wt" for overwriting, "at" for appending
        :param str encoding: The encoding of the text, e.g. "utf-8".
            Do not use "utf-8-sig" when you intend to ``write`` several times to the stream or
            you will have the BOM marker not only at the beginning, but also within the file.
        :param str newline: The characters to mark the end-of-line.
            It can be ``\\n``, ``\\r``, ``\\r\\n`` or None. When None, the system default
            value for the platform is used.
        :param callable fnLog: The callable which is called from the log method
            It expects a string parameter
        """
        self.uristring = uristring
        self.mode = mode
        if mode != "wt" and mode != "at":
            raise ValueError(
                f'UriTextOutputStream: Invalid mode "{mode}"! Valid modes are "wt" and "at"'
            )

        self.encoding = encoding
        self.newline = newline
        self._fnlog = fnLog  # for logging to user code
        self.stream = UriOutputStream(uristring, mode[0] + "b", fnLog)

    # __init__

    def __enter__(self):
        return self

    # __enter

    def __exit__(self, exc_type, exc_value, traceback):
        if self.stream is not None:
            try:
                self.close()
            except BaseException as ex:
                pass
        return False  # propagate exceptions

    # __exit__

    def close(self):
        """
        Flushes and closes the stream
        """
        if self.stream is not None:
            self.flush()
            self.stream.close()
        self.stream = None

    # close

    @property
    def closed(self):
        """
        Checks if the stream is closed

        :returns: True when closed, False otherwise
        """
        return self.stream is None

    # closed

    def read(self, maxsize=-1):
        """
        This method will raise an OS error when it is called
        """
        raise OSError(22, "not readable")

    # read

    def readinto(self, bytesobj):
        """
        This method will raise an OS error when it is called
        """
        raise OSError(22, "not readable")

    # readinto

    def readall(self):
        """
        This method will raise an OS error when it is called
        """
        raise OSError(22, "not readable")

    # readall

    def readable(self):
        """
        This method always returns False

        :returns: False
        """
        return False

    # readable

    def write(self, string):
        """
        Writes a string to the stream

        :param str string: The string to be written

        :returns: The amount of characters written
        :rtype: int
        """
        sep = self.newline
        if sep is None:
            sep = os.linesep
        string2 = string.replace("\n", sep)
        bytesobj = bytes(string2, self.encoding)
        self.stream.write(bytesobj)
        return len(string2)

    # write

    def flush(self):
        """
        Flushes the write buffer of stream if applicable
        """
        self.stream.flush()

    # flush

    def isatty(self):
        """
        This method always returns False

        :returns: False
        """
        return False

    # isatty

    def seekable(self):
        """
        Checks if the stream is seekable

        :returns: True when seekable, False otherwise
        """
        return self.stream.seekable()

    # seekable

    def truncate(self, size=None):
        """
        Resizes the stream to the given size.
        This is currently unimplemented on Android

        :param int size: The new size in bytes

        :returns: The new size in bytes
        :rtype: int
        """
        return self.stream.truncate(size)

    # truncate

    def writable(self):
        """
        Checks if the stream is writable

        :returns: True when writable, False otherwise
        """
        return self.stream.writable()

    # writable

    def log(self, message):
        """
        Logs a message to the user code if fnLog was passed to the constructor

        :param str message: The message to be logged
        """
        if self._fnlog is not None:
            self._fnlog(message)

    # log


# UriTextOutputStream


version = "0.9.0"
version_date = "2023-05-23 - 2023-05-31"
