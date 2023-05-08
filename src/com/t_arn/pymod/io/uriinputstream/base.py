import toga

class UriInputStream:
    
    def __init__(self, app, uri, fnLog=None):
        """
        Creates a UriInputStream
        
        :param toga.App app: The current App object
        :param callable fnLog: The callable which is called from the log method
            It expects a string parameter
        """
        self.uri = uri
        self.fnLog = fnLog  # for logging to user code
        if toga.platform.current_platform == "android":
            from .android import UriInputStreamImpl
        if toga.platform.current_platform == "windows":
            from .windows import UriInputStreamImpl
        self.impl = UriInputStreamImpl(self)
        
        context = Python.getPlatform().getApplication()
        self.stream = context.getContentResolver().openInputStream(uri)
    # __init__
    
    def close(self):
        self.stream.close()
        self.stream = None
    # close
    
    def closed(self):
        return self.stream is None
    # closed
    
    def read(self, maxsize=-1):
        if maxsize == -1:
            return self.readall()
    # read
    
    def readinto(byteobj):
        pass
    # readinto
    
    def readall(self):
        return bytes(self.stream.readAllBytes())
    # readall
    
    def log(self, message):
        """
        Logs a message to the user code if fnLog was passed to the constructor
        
        :param str message: The message to be logged
        """
        if self.fnLog is not None:
            self.fnLog(message)
    # log

# UriInputStreamImpl
