from android.net import Uri
import toga

class UriInputStreamImpl:
    
    def __init__(self, interface):
        self.interface = interface
        context = toga.App.app._impl.native
        uri = Uri.parse(interface.uristring)
        self.stream = context.getContentResolver().openInputStream(uri)
    # __init__
    
    # RawIOBase methods
    def read(self, maxsize):
        if maxsize == -1:
            return self.readall()
        bytesobj = self.stream.readNBytes(maxsize)
        if len(bytesobj) == 0:
            bytesobj = None
        return bytesobj
    # read
    
    def readinto(self, bytesobj):
        i = self.stream.read(bytesobj)
        if i == -1:
            i = None
        return i
    # readinto
    
    def readall(self):
        return bytes(self.stream.readAllBytes())
    # readall
    
    # IOBase methods
    def close(self):
        if self.stream is not None:
            self.stream.close()
        self.stream = None
    # close
    
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


version = "0.8.0"
version_date = "2023-05-23 - 2023-05-23"
