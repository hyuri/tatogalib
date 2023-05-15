from android.net import Uri

class UriInputStreamImpl:
    
    def __init__(self, interface):
        self.interface = interface
        self.eof = False
        context = interface.app._impl.native
        uri = Uri.parse(interface.uristring)
        self.stream = context.getContentResolver().openInputStream(uri)
    # __init__
    
    # RawIOBase methods
    def read(self, maxsize):
        if maxsize == -1:
            return self.readall()
        bytesobj = self.stream.readNbytes(maxsize)
        if len(bytesobj == 0:
            self.eof = True
            bytesobj = None
        return bytesobj
    # read
    
    def readinto(self, bytesobj):
        i = self.stream.read(bytesobj)
        if i == -1:
            self.eof = True
            i = None
        return i
    # readinto
    
    def readall(self):
        self.eof = True
        return bytes(self.stream.readAllBytes())
    # readall
    
    # IOBase methods
    def close(self):
        if self.stream is not None:
            self.stream.close()
        self.stream = None
    # close
    
    @property
    def closed(self):
        return self.stream is None
    # closed

    def fileno(self):
        raise OSError(9, "No file descriptor available")
    # fileno
    
    def readable(self):
        return True
    # readable
        
    def seekable(self):
        return False
    # seekable
    
    def seek(self, offset, whence=0):
        raise OSError(22, "not seekable")
    # seek
    
    def tell(self):
        raise OSError(22, "not seekable")
    # tell

# UriInputStreamImpl
