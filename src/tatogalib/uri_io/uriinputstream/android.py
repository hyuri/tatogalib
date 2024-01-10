from android.net import Uri
from java.lang import Integer
import toga


class UriInputStreamImpl:
    def __init__(self, interface):
        self.interface = interface
        context = toga.App.app._impl.native
        uri = Uri.parse(interface.uristring)
        self.stream = context.getContentResolver().openInputStream(uri)
        self.buffer = bytearray(4096)

    # __init__

    # RawIOBase methods
    def read(self, maxsize):
        # readNBytes() is only available on API 33 or later
        # So, we use our own implementation here
        if maxsize == -1:
            maxsize = Integer.MAX_VALUE
        bytesobj = b""
        remaining = maxsize
        try:
            while remaining > 0:
                i = self.stream.read(self.buffer)
                if i == -1:
                    break
                else:
                    if i > remaining:
                        i = remaining
                    bytesobj += self.buffer[0: i]
                    remaining -= i
        except BaseException as ex:
            bytesobj = None
            self.interface.log(str(ex))
        finally:
            return bytesobj

    # read

    def readinto(self, bytesobj):
        i = self.stream.read(bytesobj)
        if i == -1:
            i = None
        return i

    # readinto

    def readall(self):
        return self.read(-1)

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

    def writable(self):
        return False

    # writable


# UriInputStreamImpl


version = "0.8.0"
version_date = "2023-05-23 - 2023-05-23"
