import toga
import io

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
    
    def seekable(self):
        """
        Checks if the stream is seekable
                
        :returns: True when seekable, False otherwise
        """
        return self._impl.seekable()
    # seekable

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

# UriInputStream


class UriTextInputStream():
    
    def __init__(self, uristring, encoding, fnLog=None):
        """
        Creates a UriTextInputStream which wraps a TextIOWrapper.
        Valid line endings are \\n, \\r or \\n\\r. They are all 
        translated to \\n.
        This class supports the context manager protocol.
        
        :param str uristring: The URI-string of the stream
        :param str encoding: The encoding of the text
        :param callable fnLog: The callable which is called from the log method
            It expects a string parameter
        """
        self.uristring = uristring
        self.encoding = encoding
        self._fnlog = fnLog  # for logging to user code
        self.log("create UriInputStream")
        self._raw = UriInputStream(uristring, fnLog)
        self.log("create io.BufferedReader")
        self._br = io.BufferedReader(self._raw)
        self.log("create io.TextIOWrapper")
        self.stream = io.TextIOWrapper(self._br, encoding=encoding, errors=None, newline=None, line_buffering=False, write_through=False)
    # __init__

    def __enter__(self):
        return self
    # __enter
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.stream is not None:
            self.close()
        return False  # propagate exceptions
    # __exit__
    
    def close(self):
        """
        Closes the stream
        """
        if self.stream is not None:
            self._raw.close()
            self._br.close()
            self.stream.close()
        self.stream = None
    # close
    
    @property
    def closed(self):
        """
        Checks if the stream is closed
        
        :returns: True when closed, False otherwise
        """
        return self.stream.closed()
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
        self.log("read()")
        return self.stream.read(maxsize)
    # read
    
    def readinto(self, bytesobj):
        """
        Read bytes into the byte-like object
        
        :param bytes bytesobj: The byte-like object to read into
        
        :returns: the number of bytes read or None when no more bytes available
        :rtype: int or None
        """
        return self.stream.readinto(bytesobj)
    # readinto
    
    def readall(self):
        """
        Reads all available bytes
        
        :returns: the read bytes
        :rtype: bytes
        """
        return self.stream.readall()
    # readall
    
    def readable(self):
        """
        Checks if the stream is readable
        
        :returns: True when readable, False otherwise
        """
        return self.stream.readable()
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

    def seekable(self):
        """
        Checks if the stream is seekable
                
        :returns: True when seekable, False otherwise
        """
        return self.stream.seekable()
    # seekable

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

# UriTextInputStream


version = "0.9.0"
version_date = "2023-05-23 - 2023-05-30"
