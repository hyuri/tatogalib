import toga

class UriInputStream:
    
    def __init__(self, uristring, fnLog=None):
        """
        Creates a UriInputStream which wraps a RawIOBase stream.
        This class supports the context manager protocol.
        
        :param str uristring: The URI-string of the stream
        :param callable fnLog: The callable which is called from the log method
            It expects a string parameter
        """
        self.uristring = uristring
        self._fnlog = fnLog  # for logging to user code
        self._impl = None
        if toga.platform.current_platform == "android":
            from .android import UriInputStreamImpl
        if toga.platform.current_platform == "windows":
            from .desktop import UriInputStreamImpl
        self._impl = UriInputStreamImpl(self)
    # __init__
    
    def __enter__(self):
        return self
    # __enter
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self._impl is not None:
            self.close()
        return False  # propagate exceptions
    # __exit__
    
    def close(self):
        """
        Closes the stream
        """
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
        Reads maxsize bytes from the stream. If less than maxbytes are returned,
        we reached the end of the stream
        
        :param int maxsize: the amount of bytes to read. When -1, all available
            bytes are read
            
        :returns: the read bytes
        :rtype: bytes
        """
        return self._impl.read(maxsize)
    # read
    
    def readinto(self, bytesobj):
        """
        Read bytes into the byte-like object
        
        :param bytes bytesobj: The byte-like object to read into
        
        :returns: the number of bytes read or None when no more bytes available
        :rtype: int or None
        """
        return self._impl.readinto(bytesobj)
    # readinto
    
    def readall(self):
        """
        Reads all available bytes
        
        :returns: the read bytes
        :rtype: bytes
        """
        return self._impl.readall()
    # readall
    
    def readable(self):
        """
        Checks if the stream is readable
        
        :returns: True when readable, False otherwise
        """
        return self._impl.readable()
    # readable
    
    def write(self, bytesobj):
        """
        This method will raise an OS error when it is called
        """
        raise OSError(22, "not writable")
    # write

    def flush(self):
        """
        This method is doing nothing on this stream
        """
        pass
    # flush
    
    def isatty(self):
        """
        This method always returns False
        
        :returns: False
        """
        return False
    # isatty
        
    def truncate(self, size=None):
        """
        This method will raise an OS error when it is called
        """
        raise OSError(22, "not writable")
    # truncate

    def writable(self):
        """
        This method always returns False
        """
        return False
    # writable

    def log(self, message):
        """
        Logs a message to the user code if fnLog was passed to the constructor
        
        :param str message: The message to be logged
        """
        if self._fnlog is not None:
            self._fnlog(message)
    # log

# UriInputStreamImpl


version = "0.8.0"
version_date = "2023-05-23 - 2023-05-23"
