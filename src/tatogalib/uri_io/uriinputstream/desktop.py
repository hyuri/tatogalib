from .. import urifile


class UriInputStreamImpl:
    def __init__(self, interface):
        self.interface = interface
        ospath = urifile.uristring_to_ospath(interface.uristring)
        self.stream = open(ospath, "rb", buffering=0)

    # __init__

    # RawIOBase methods
    def read(self, maxsize):
        return self.stream.read(maxsize)

    # read

    def readinto(self, bytesobj):
        return self.stream.readinto(bytesobj)

    # readinto

    def readall(self):
        return self.stream.readall()

    # readall

    # IOBase methods
    def close(self):
        self.stream.close()
        self.stream = None

    # close

    def closed(self):
        return self.stream is None

    # closed

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


# UriInputStreamImpl


version = "0.8.0"
version_date = "2023-05-23 - 2023-05-23"
