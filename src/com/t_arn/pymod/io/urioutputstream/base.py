import toga

class UriOutputStream:
    
    def __init__(self, app, uristring, mode, fnLog=None):
        """
        Creates a UriOutputStream
        
        :param toga.App app: The current App object
        :param str uristring: The URI-string of the stream
        :param str mode: "w" for overwriting, "a" for appending
        :param callable fnLog: The callable which is called from the log method
            It expects a string parameter
        """
        self.app = app
        self.uristring = uristring
        self.mode = mode
        self.fnLog = fnLog  # for logging to user code
        if toga.platform.current_platform == "android":
            from .android import UriOutputStreamImpl
        if toga.platform.current_platform == "windows":
            from .desktop import UriOutputStreamImpl
        self.impl = UriOutputStreamImpl(self, mode)
    # __init__
    
    def close(self):
        self.flush()
        self.impl.close()
    # close
    
    def closed(self):
        return self.impl.closed
    # closed
    
    def read(self, maxsize=-1):
        raise OSError(22, "not readable")
    # read
    
    def readinto(bytesobj):
        raise OSError(22, "not readable")
    # readinto
    
    def readall(self):
        raise OSError(22, "not readable")
    # readall
    
    def readable(self):
        return False
    # readable
    
    def write(self, bytesobj):
        return self.impl.write(bytesobj)
    # write

    def flush(self):
        self.impl.flush()
    # flush
    
    def isatty(self):
        return False
    # isatty
        
    def truncate(self, size=None):
        return impl.truncate(size)
    # truncate

    def writable(self):
        return True
    # writable

    def log(self, message):
        """
        Logs a message to the user code if fnLog was passed to the constructor
        
        :param str message: The message to be logged
        """
        if self.fnLog is not None:
            self.fnLog(message)
    # log

# UriOutputStreamImpl
