from ..urifile import UriFile
from android.net import Uri
from java.lang import Integer
import os
import toga


class UriInputStreamImpl:
    def __init__(self, interface):
        self.interface = interface
        self.buffer = bytearray(4096)
        self.position = 0
        urifile = UriFile(self.interface.uristring)
        self.seek_end_offset = urifile.size
        print(f"stream seek_end={self.seek_end_offset}")
        self.stream = None
        self._open_stream()
    # __init__

    def _open_stream(self):
        context = toga.App.app._impl.native
        uri = Uri.parse(self.interface.uristring)
        self.stream = context.getContentResolver().openInputStream(uri)
        self.position = 0
    # _open_stream

    # RawIOBase methods
    def read(self, maxsize):
        # readNBytes() is only available on API 33 or later
        # So, we use our own implementation here
        print(f"read({maxsize}), position={self.position}")
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
            self.position += len(bytesobj)
            print(f"read {len(bytesobj)} bytes, new position={self.position}")
        except BaseException as ex:
            bytesobj = None
            print(str(ex))
            self.interface.log(str(ex))
        finally:
            return bytesobj

    # read

    def readinto(self, bytesobj):
        i = self.stream.read(bytesobj)
        if i == -1:
            i = None
        else:
            self.position += i
            print(f"readinto(len={len(bytesobj)}), new position={self.position}")
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
        return True

    # seekable

    def seek(self, offset, whence):
        print(f"UriInputStream.seek({offset}, {whence})")
        if whence == os.SEEK_SET:
            start = 0
        if whence == os.SEEK_CUR:
            start = self.position
        if whence == os.SEEK_END:
            start = self.seek_end_offset
        absolut_offset = start + offset
        print(f"absolut_offset={absolut_offset}")
        # if absolut_offset < self.position:
        # todo: undo
        if absolut_offset >=0 and absolut_offset <= self.seek_end_offset:
            # This is very inefficient, but (to my knowledge) there is no other way 
            self.stream.close()
            self._open_stream()
            if absolut_offset == 0:
                print("no skipping needed")
            else:
                print(f"skipping {absolut_offset}")
                i = self.stream.skip(absolut_offset)
                if i != absolut_offset:
                    raise OSError("UriInputStream.seek() did not set the requested position")
        else:
            # todo: remove
            # skipping ahead without prior closing did not work
            # for reading ZipFiles.
            relative_offset = absolut_offset - self.position
            if relative_offset == 0:
                print("no skipping needed")
            else:
                print(f"skipping {relative_offset}")
                i = self.stream.skip(relative_offset)
                if i != relative_offset:
                    raise OSError("UriInputStream.seek() did not set the requested position")
        self.position = absolut_offset
        print(f"new position={absolut_offset}")
    # seek

    def tell(self):
        return self.position

    # tell

    def writable(self):
        return False

    # writable


# UriInputStreamImpl


version = "0.9.0"
version_date = "2023-05-23 - 2024-05-04"
