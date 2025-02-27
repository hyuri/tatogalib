from pathlib import Path
from ... import system
from ..uriinputstream import UriInputStream, UriTextInputStream
from ..urioutputstream import UriOutputStream, UriTextOutputStream


if system.get_platform() == "android":
    from .android import UriFileImpl
elif system.get_platform() in ("windows", "linux", "macOS"):
    from .desktop import UriFileImpl
else:
    raise NotImplementedError(f"UriFile is not implemented for {system.get_platform()}")


class UriFile:
    def __init__(self, uristring, fnLog=None):
        """
        Creates a UriFile which represents a file or a folder

        :param str uristring: A URI-string representing this UriFile object
        :param callable fnLog: The callable which is called from the log method
            It expects a string parameter
        """
        self.uristring = uristring
        self._fnlog = fnLog  # for logging to user code
        self._impl = UriFileImpl(self)

    # __init__

    def __str__(self):
        return self._impl.__str__()

    def __truediv__(self, child):
        return self._impl.__truediv__(child)

    @property
    def name(self):
        """
        The name (str) of the file or folder
        """
        return self._impl.get_name()
    
    @property
    def stem(self):
        """
        The stem (str) of the file or folder
        """
        return self._impl.get_stem()
    
    @property
    def suffix(self):
        """
        The suffix (str) of the file or folder
        """
        return self._impl.get_suffix()
    
    @property
    def parent(self):
        """
        The parent folder
        """
        return self._impl.get_parent()

    def with_suffix(self, suffix):
        return self._impl.with_suffix(suffix)

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

    def create_file(self, child_name, replace=False):
        """
        Creates a new file with a length of 0 bytes in the folder represented by this
        UriFile. If this UriFile is not a folder, a NotADirectoryError will be raised.

        :param str child_name: The name of the file to be created
        :param boolean replace: When true, an existing file with the
            child_name will be replaced. When False, a FileExistsError
            is raised in this case.

        :returns: The newly created file
        :rtype: UriFile
        """
        if not self.is_dir():
            raise NotADirectoryError("UriFile is not an accessible directory.")
        urifile = self.find(child_name)
        if urifile is not None:
            if urifile.is_file():
                if not replace:
                    raise FileExistsError(f"File '{child_name}' already exists!")
                else:
                    urifile.delete()
            else:
                raise IsADirectoryError(f"Directory '{child_name}' already exists!")
        uristring = self._impl.create_file(child_name)
        return UriFile(uristring, self._fnlog)

    # create_file

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

    def find(self, child_name):
        """
        Returns the child file or folder of the folder represented by this UriFile.
        If this UriFile is not a folder, a NotADirectoryError will be raised.

        :param str child_name: The name of the file or folder to find

        :returns: The child if it exists, None otherwise
        :rtype: UriFile or None
        """
        if not self.is_dir():
            raise NotADirectoryError("UriFile is not an accessible directory")
        uristring = self._impl.find(child_name)
        if uristring is None:
            return None
        return UriFile(uristring, self._fnlog)

    # find

    @staticmethod
    def from_path(path):
        """
        Creates a new instance of Urifile from a pathlib Path.
        Return None if the Path does not exist.
        Raises a TypeError when path is not a Path object

        :param Path path: The path representing a file or folder
        :returns: A new Urifile or None
        :rtype: UriFile or None
        """
        if not isinstance(path, Path):
            raise TypeError(
                "Urifile.from_path() requires an argument of type pathlib.Path"
            )
        return UriFileImpl.from_path(path)

    # from_path

    def get_path(self):
        """
        Gets the pathlib Path of this UriFile.
        Returns None if the Path cannot be determined.

        :returns: The Path or None
        :rtype: Path or None
        """
        return self._impl.get_path()

    # get_path

    def get_authorized_uristring(self):
        """
        Get the uristring to access this UriFile based on existing persisted folder permissions.
        This is only relevant for Android and will return this UriFile's uristring on other platforms.
        When no matching permissions are found, None will be returned.

        :returns: uristring for this UriFile or None
        """
        return self._impl.get_authorized_uristring()

    # get_authorized_uristring

    @staticmethod
    def get_persisted_permissions():
        """
        Get the persisted permissions to files or folders.
        This is only relevant for Android and will return an empty list on other platforms.

        :returns: list with permissions
        """
        return UriFileImpl.get_persisted_permissions()

    # get_persisted_permissions

    def get_uristring(self):
        """
        Get the uristring of this UriFile.

        :returns: uristring for this UriFile
        :rtype: str
        """
        return self.uristring

    # get_uristring

    def is_dir(self):
        """
        Checks if the UriFile represents an existing folder

        :returns: True or False
        :rtype: boolean
        """
        return self._impl.is_dir()
    
    def isdir(self):
        """
        (Backward Compatibility) Checks if the UriFile represents an existing folder

        :returns: True or False
        :rtype: boolean
        """
        return self._impl.is_dir()

    # is_dir

    def is_file(self):
        """
        Checks if the UriFile represents an existing file

        :returns: True or False
        :rtype: boolean
        """
        return self._impl.is_file()
    
    def isfile(self):
        """
        (Backward Compatibility) Checks if the UriFile represents an existing file

        :returns: True or False
        :rtype: boolean
        """
        return self._impl.is_file()

    # is_file

    def listdir(self):
        """
        Returns a list of all UriFiles contained in the folder represented
        by this UriFile. When there are no children, an empty list is
        returned. If this UriFile is not a folder, None will be returned.

        :returns: The children of this UriFile
        :rtype: A list of UriFiles or None
        """
        if not self.is_dir():
            return None
        result = []
        children = self._impl.listdir()
        for uristring in children:
            urifile = UriFile(uristring, self._fnlog)
            result.append(urifile)
        return result

    # listdir

    def log(self, message):
        """
        Logs a message to the user code if fnLog was passed to the constructor

        :param str message: The message to be logged
        """
        if self._fnlog is not None:
            self._fnlog(message)

    # log

    def open(self, mode = "r", encoding="utf-8", newline=None):
        """
        Opens a binary or text stream for reading or writing.
        The ``mode`` parameter must contain the operation and the data type of the stream to open.
        Valid operations are (r)ead, (w)rite and (a)ppend. Valid data types are (b)inary and (t)ext. Default is "r", which is a synonym for "rt".
        ``encoding`` is only relevant when opening text streams for reading or writing.
        ``newline`` is only relevant when opening a text stream for writing.
        When reading from a text stream, ``newline`` is ignored and all kinds of newline characters
        are converted to ``\\n``.

        :param str mode: The mode for opening a stream, e.g. "wt"
        :param str encoding: The encoding to use for converting the text to bytes, e.g. "utf-8-sig"
        :param str newline: The characters to mark the end-of-line.
            It can be ``\\n``, ``\\r``, ``\\r\\n`` or None. When None, the system default
            value is used when writing to a text stream.

        :returns: The stream to open
        :rtype: UriInputStream, UriTextInputStream, UriOutputStream or UriTextOutputStream
        """
        (operation, data_type) = self._validate_open_mode(mode)
        mode = operation + data_type

        r_mode = operation == "r" and data_type == ""
        rt_mode = operation == "r" and data_type == "t"
        wa_mode = operation in "wa" and data_type == ""
        wat_mode = operation in "wa" and data_type == "t"
        
        # "r" is a synonym for "rt" | In other words: the "t" data type is the default
        if r_mode or rt_mode:
            return UriTextInputStream(self.uristring, encoding, self._fnlog)
        
        elif operation == "r" and data_type == "b":
            return UriInputStream(self.uristring, self._fnlog)
        
        # "w" and "a" are synonyms for "wt" and "at", respectively | In other words: the "t" data type is the default
        elif wa_mode or wat_mode:
            mode = operation + "t"
            return UriTextOutputStream(self.uristring, mode, encoding, newline, self._fnlog)
        
        elif operation in "wa" and data_type == "b":
            mode = operation + "b"
            return UriOutputStream(self.uristring, mode, self._fnlog)

    # open

    def _validate_open_mode(self, mode):
        errmsg = (
            f'Invalid mode "{mode}"! Valid modes are "r" | "rt" | "r+t" (default), "w" | "wt" | "w+t", "a" | "at" | "a+t", "rb" | "r+b", "wb" | "w+b", "ab" | "a+b"'
        )
        
        operation = ""
        data_type = ""

        if "+" in mode:
            (operation, data_type) = mode.split("+", 1)
        
        elif len(mode) == 1:
            if mode in "rwa":
                operation = mode
            else:
                raise ValueError(errmsg)
        
        else:
            for c in mode:
                if c in "rwa":
                    operation += c
                elif c in "bt":
                    data_type += c
                else:
                    raise ValueError(errmsg)
        
        if len(operation) != 1 or len(data_type) not in {0, 1}:
            raise ValueError(errmsg)
        
        return (operation, data_type)

    # _validate_open_mode

    def release_persistent_access(self, read=True, write=True):
        """
        Release a permanent access to the file or folder.
        This is only relevant for Android and is ignored on other platforms.

        :param bool read: Release read permissions
        :param bool write: Release write permissions
        """
        if system.get_platform() == "android":
            self._impl.release_persistent_access(read, write)

    # release_persistent_access

    def request_persistent_access(self, read=True, write=True):
        """
        Get permanent access to the file or folder.
        This is only relevant for Android and is ignored on other platforms.

        :param bool read: Request read permissions
        :param bool write: Request write permissions
        """
        if system.get_platform() == "android":
            self._impl.request_persistent_access(read, write)

    # request_persistent_access


# UriFile


version = "0.8.0"
version_date = "2023-05-23 - 2023-12-20"
