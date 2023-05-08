class UriInputStreamImpl:
    
    def __init__(self, interface, uri):
        self.interface = interface
        self.uri = uri
        context = interface.app._impl.native
        self.stream = context.getContentResolver().openInputStream(uri)
    # __init__
    
    def close(self):
        if self.stream is not None:
            self.stream.close()
        self.stream = None
    # close
    
    @property
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
    
    
# UriInputStreamImpl
