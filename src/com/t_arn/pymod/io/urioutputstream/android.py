from android.net import Uri

class UriOutputStreamImpl:
    
    def __init__(self, interface, mode):
        self.interface = interface
        if mode == "a":
            mode = "wa"
        self.mode = mode
        self.eof = False
        context = interface.app._impl.native
        uri = Uri.parse(interface.uristring)
        self.stream = context.getContentResolver().openOutputStream(uri, mode)
    # __init__
    
    # RawIOBase methods
    def write(self, bytesobj):
        self.stream.write(bytesobj)
    # wtite
    
    # IOBase methods
    def close(self):
        if self.stream is not None:
            self.stream.close()
        self.stream = None
    # close
    
    def flush(self):
        self.stream.flush()
    # flush
    
    @property
    def closed(self):
        return self.stream is None
    # closed

    def fileno(self):
        raise OSError(9, "No file descriptor available")
    # fileno
    
    def readable(self):
        return False
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
    
    def truncate(self, size=None):
        pass  # todo: implement
    # truncate

# UriOutputStreamImpl
