from .. import urifile
from .. import _security_scoped_urls


class UriOutputStreamImpl:
    def __init__(self, interface, mode):
        self.interface = interface
        self._nsurl = _security_scoped_urls.get(interface.uristring)
        if self._nsurl is not None:
            try:
                self._nsurl.startAccessingSecurityScopedResource()
            except Exception:
                self._nsurl = None
        ospath = urifile.uristring_to_ospath(interface.uristring)
        if ospath is None:
            from urllib.parse import urlparse, unquote
            pr = urlparse(interface.uristring)
            ospath = unquote(pr.path)
        self.stream = open(ospath, mode, buffering=0)

    def write(self, bytesobj):
        self.stream.write(bytesobj)
        return len(bytesobj)

    def close(self):
        if self._nsurl is not None:
            try:
                self._nsurl.stopAccessingSecurityScopedResource()
            except Exception:
                pass
            self._nsurl = None
        if self.stream is not None:
            self.flush()
            self.stream.close()
        self.stream = None

    def flush(self):
        if self.stream is not None:
            self.stream.flush()

    def closed(self):
        return self.stream is None

    def fileno(self):
        return self.stream.fileno()

    def readable(self):
        return False

    def seekable(self):
        return False

    def seek(self, offset, whence=0):
        raise OSError(22, "not seekable")

    def tell(self):
        raise OSError(22, "not seekable")

    def truncate(self, size=None):
        return self.stream.truncate(size)

    def writable(self):
        return True
