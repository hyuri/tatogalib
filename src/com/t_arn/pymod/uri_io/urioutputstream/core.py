import toga

class UriOutputStream:
    
    def __init__(self, app, uristring, mode, fnLog=None):
        """
        Creates a UriOutputStream which wraps a RawIOBase stream
        
        :param toga.App app: The current App object
        :param str uristring: The URI-string of the stream
        :param str mode: "w" for overwriting, "a" for appending
        :param callable fnLog: The callable which is called from the log method
            It expects a string parameter
        """
        self.app = app
        self.uristring = uristring
        self.mode = mode
        self._fnlog = fnLog  # for logging to user code
        if toga.platform.current_platform == "android":
            from .android import UriOutputStreamImpl
        if toga.platform.current_platform == "windows":
            from .desktop import UriOutputStreamImpl
        self._impl = UriOutputStreamImpl(self, mode)
    # __init__
    
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
    
    def readinto(bytesobj):
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
        """
        return False
    # readable
    
    def write(self, bytesobj):
        """
        Writes bytes to the stream
        
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
        """
        return False
    # isatty
        
    def truncate(self, size=None):
        """
        Resizes the stream to the given size.
        This is currently unimplemented on Android
        
        :returns: The new size in bytes
        :rtype: int
        """
        return _impl.truncate(size)
    # truncate

    def writable(self):
        """
        This method always returns True
        """
        return True
    # writable

    def log(self, message):
        """
        Logs a message to the user code if fnLog was passed to the constructor
        
        :param str message: The message to be logged
        """
        if self._fnlog is not None:
            self._fnlog(message)
    # log

# UriOutputStreamImpl


version = "0.8.0"
version_date = "2023-05-23 - 2023-05-23"
