from .. import urifile

class UriOutputStreamImpl:
    
    def __init__(self, interface, mode):
        self.interface = interface
        ospath = urifile.uristring_to_ospath(interface.uristring)
        mode = mode + "b"
        self.stream = open(ospath, mode, buffering=0)
    # __init__
    
    # RawIOBase methods
    def write(self, bytesobj):
        self.stream.write(bytesobj)
    # wtite
    
    # IOBase methods
    def close(self):
        self.stream.close()
        self.stream = None
    # close
    
    def closed(self):
        return self.stream.closed
    # closed
    
    def flush(self): 
        self.stream.flush()
    # flush

    def fileno(self):
        return self.stream.fileno()
    # fileno
    
    def readable(self):
        return self.stream.readable()
    # readable
        
    def seekable(self):
        return self.stream.seekable()
    # seekable
    
    def seek(self, offset, whence=0):
        self.stream.seek(offset, whence)
    # seek
    
    def tell(self):
        return self.stream.tell()
    # tell

    def truncate(self, size=None):
        return self.stream.truncate(size)
    # truncate

# UriOutputStreamImpl


version = "0.8.0"
version_date = "2023-05-23 - 2023-05-23"
