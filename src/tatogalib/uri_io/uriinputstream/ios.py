from .. import urifile


class UriInputStreamImpl:
    def __init__(self, interface):
        self.interface = interface
        ospath = urifile.uristring_to_ospath(interface.uristring)
        if ospath is None:
            from urllib.parse import urlparse, unquote
            pr = urlparse(interface.uristring)
            ospath = unquote(pr.path)
        self.stream = open(ospath, "rb", buffering=0)

    def read(self, maxsize):
        return self.stream.read(maxsize)

    def readinto(self, bytesobj):
        return self.stream.readinto(bytesobj)

    def readall(self):
        return self.stream.readall()

    def close(self):
        if self.stream is not None:
            self.stream.close()
        self.stream = None

    def closed(self):
        return self.stream is None

    def fileno(self):
        return self.stream.fileno()

    def readable(self):
        return True

    def seekable(self):
        return self.stream.seekable()

    def seek(self, offset, whence):
        self.stream.seek(offset, whence)

    def tell(self):
        return self.stream.tell()

    def writable(self):
        return False
