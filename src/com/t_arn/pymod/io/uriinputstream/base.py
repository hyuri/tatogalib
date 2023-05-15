import toga

class UriInputStream:
    
    def __init__(self, app, uristring, fnLog=None):
        """
        Creates a UriInputStream
        
        :param toga.App app: The current App object
        :param str uristring: The URI-string of the stream
        :param callable fnLog: The callable which is called from the log method
            It expects a string parameter
        """
        self.uristring = uristring
        self.fnLog = fnLog  # for logging to user code
        if toga.platform.current_platform == "android":
            from .android import UriInputStreamImpl
        if toga.platform.current_platform == "windows":
            from .desktop import UriInputStreamImpl
        self.impl = UriInputStreamImpl(self)
    # __init__
    
    def close(self):
        self.impl.close()
    # close
    
    def closed(self):
        return self.impl.closed
    # closed
    
    def read(self, maxsize=-1):
        return self.impl.read(maxsize)
    # read
    
    def readinto(bytesobj):
        return self.impl.readinto(bytesobj)
    # readinto
    
    def readall(self):
        return self.impl.readall()
    # readall
    
    def readable(self):
        return self.impl.readable()
    # readable
    
    def write(self, bytesobj):
        raise OSError(22, "not writable")
    # write

    def flush(self):
        pass
    # flush
    
    def isatty(self):
        return False
    # isatty
        
    def truncate(self, size=None):
        raise OSError(22, "not writable")
    # truncate

    def writable(self):
        return False
    # writable

    def log(self, message):
        """
        Logs a message to the user code if fnLog was passed to the constructor
        
        :param str message: The message to be logged
        """
        if self.fnLog is not None:
            self.fnLog(message)
    # log

# UriInputStreamImpl
