import toga
from ..uriinputstream import UriInputStream, UriTextInputStream
from ..urioutputstream import UriOutputStream, UriTextOutputStream


class UriFile:
    def __init__(self, uristring, is_file=True, fnLog=None):
        """
        Creates a UriFile which represents a file or a folder

        :param str uristring: A URI-string representing this UriFile object
        :param boolean is_file: True when uristring represents a file, False for a folder
        :param callable fnLog: The callable which is called from the log method
            It expects a string parameter
        """
        self.uristring = uristring
        self._fnlog = fnLog  # for logging to user code
        if toga.platform.current_platform == "android":
            from .android import UriFileImpl
        if toga.platform.current_platform == "windows":
            from .desktop import UriFileImpl
        self._impl = UriFileImpl(self, is_file)

    # __init__

    @property
    def display_name(self):
        """
        The name (str) of the file or folder
        """
        return self._impl.get_display_name()

    # display_name

    @property
    def lastmodified(self):
        """
        The last modification time (int) of the file or folder.
        It is the amount of seconds since 1970-01-01T00:00:00
        """
        return self._impl.get_lastmodified()

    def set_lastmodified(self, unixtime):
        """
        Sets the last modification time (int) of the file or folder.
        This is currently not working on Android.

        :param int unixtime: amount of seconds since 1970-01-01T00:00:00

        :returns: True on success, False on failure
        :rtype: boolean
        """
        return self._impl.set_lastmodified(unixtime)

    # lastmodified

    @property
    def mime_type(self):
        """
        The MIME type (e.g. "application/pdf") of the file.
        It is None if the MIME type cannot be evaluated.
        """
        return self._impl.get_mime_type()

    # mime_type

    @property
    def size(self):
        """
        The size (int) of the file in bytes.
        """
        return self._impl.get_size()

    # size

    def copy_to(self, urifile):
        """
        Copy the binary file represented by this UriFile to the file
        represented by urifile.

        :param UriFile urifile: The target file

        :returns: True on success, False on failure
        :rtype: boolean
        """
        buffer = None
        instream = None
        outstream = None
        result = True
        try:
            instream = self.open("rb")
            outstream = urifile.open("wb")
            while True:
                buffer = instream.read(4096)
                if len(buffer) > 0:
                    outstream.write(buffer)
                if len(buffer) < 4096:
                    break
            instream.close()
            instream = None
            outstream.flush()
            outstream.close()
            outstream = None
        except BaseException as ex:
            if instream is not None:
                instream.close()
            if outstream is not None:
                outstream.flush()
                outstream.close()
            urifile.delete()
            result = False
            self.log(str(ex))
        finally:
            return result

    # copy_to

    def delete(self):
        """
        Deletes the file

        :returns: True on success, False on failure
        :rtype: boolean
        """
        return self._impl.delete()

    # delete

    def exists(self):
        """
        Checks if the file or folder exists

        :returns: True when exists, False otherwise
        :rtype: boolean
        """
        return self._impl.exists()

    # exists

    def isdir(self):
        """
        Checks if the UriFile represents an existing folder

        :returns: True or False
        :rtype: boolean
        """
        return self._impl.isdir()

    # isdir

    def isfile(self):
        """
        Checks if the UriFile represents an existing file

        :returns: True or False
        :rtype: boolean
        """
        return self._impl.isfile()

    # isfile

    def log(self, message):
        """
        Logs a message to the user code if fnLog was passed to the constructor

        :param str message: The message to be logged
        """
        if self._fnlog is not None:
            self._fnlog(message)

    # log

    def _open_raw_inputstream(self):
        """
        Opens a rawIO stream for reading from the file represented by this UriFile

        :returns: the binary stream to read from
        :rtype: UriInputStream (RawIOBase)
        """
        return UriInputStream(self.uristring, self._fnlog)

    # _open_raw_inputstream

    def _open_raw_outputstream(self, mode):
        """
        Opens a rawIO stream for writing to the file represented by this UriFile

        :param str mode: "wb" for overwriting, "ab" for appending

        :returns: the binary stream to write to
        :rtype: UriOutputStream (RawIOBase)
        """
        return UriOutputStream(self.uristring, mode, self._fnlog)

    # _open_raw_outputstream

    def _open_text_inputstream(self, encoding):
        """
        Opens a text stream for reading from the file represented by this UriFile

        :param str encoding: The encoding to use for converting the bytes to text,
            e.g. "utf-8-sig"

        :returns: the text stream to read from
        :rtype: UriTextInputStream (TextIOWrapper)
        """
        return UriTextInputStream(self.uristring, encoding, self._fnlog)

    # _open_text_inputstream

    def _open_text_outputstream(self, mode, encoding, newline=None):
        """
        Opens a text stream for writing to the file represented by this UriFile

        :param str mode: "wt" for overwriting, "at" for appending
        :param str encoding: The encoding to use for converting the text to bytes,
            e.g. "utf-8"
        :param str newline: The characters to mark the end-of-line.
            It can be ``\\n``, ``\\r``, ``\\r\\n`` or None. When None, the system default
            value is used.

        :returns: the text stream to write to
        :rtype: UriTextOutputStream
        """
        return UriTextOutputStream(self.uristring, mode, encoding, newline, self._fnlog)

    # _open_text_outputstream

    def open(self, mode, encoding, newline=None):
        """
        Opens a binary or text stream for reading or writing.
        The ``mode`` parameter must contain the operation and the data type of the stream to open.
        Valid operations are (r)ead, (w)rite and (a)ppend. Valid data types are (b)inary and (t)ext.
        ``encoding`` is only relevant opening text streams for reading or writing.
        ``newline`` is only relevant when opening a text stream for writing.
        When reading from a text stream, ``newline`` is ignored and all kinds of newline characters
        are converted to ``\\n``.

        :param str mode: The mode for opening a stream, e.g. "wt"
        :param str encoding: The encoding to use for converting the text to bytes, e.g. "utf-8"
        :param str newline: The characters to mark the end-of-line.
            It can be ``\\n``, ``\\r``, ``\\r\\n`` or None. When None, the system default
            value is used when writing to a text stream.

        :returns: The stream to open
        :rtype: UriInputStream, UriTextInputStream, UriOutputStream or UriTextOutputStream
        """
        (operation, data_type) = self._validate_open_mode(mode)
        if operation == "r" and data_type == "b":
            return self._open_raw_inputstream()
        elif operation == "r" and data_type == "t":
            return self._open_text_inputstream(encoding)
        elif operation in "wa" and data_type == "b":
            return self._open_raw_outputstream(operation + data_type)
        elif operation in "wa" and data_type == "t":
            return self._open_text_outputstream(
                operation + data_type, encoding, newline
            )
        # open

    def _validate_open_mode(mode):
        valid_modes = '"rb", "rt", "wb", "wt", "ab", "at"'
        operation = ""
        data_type = ""
        for c in mode:
            if c == "w" or c == "r" or c == "a":
                operation = operation + c
            elif c == "b" or c == "t":
                data_type = data_type + c
            else:
                raise ValueError(f"Invalid mode! {valid_modes}")
        if len(operation) != 1 or len(data_type) != 1:
            raise ValueError(f"Invalid mode! {valid_modes}")
        return (operation, data_type)

    # _validate_open_mode


# UriFile


version = "0.6.0"
version_date = "2023-05-23 - 2023-05-31"
