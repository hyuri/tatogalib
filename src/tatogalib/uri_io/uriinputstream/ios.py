from pathlib import Path

from rubicon.objc import Block, ObjCClass

from .. import urifile
from .. import _security_scoped_urls

NSURL = ObjCClass('NSURL')
NSFileCoordinator = ObjCClass('NSFileCoordinator')


class UriInputStreamImpl:
    def __init__(self, interface):
        self.interface = interface
        self._nsurl = _security_scoped_urls.get(interface.uristring)
        if self._nsurl is None:
            self._nsurl = _find_parent_nsurl(interface.uristring)
        self._security_scope_started = False
        if self._nsurl is not None:
            try:
                if self._nsurl.startAccessingSecurityScopedResource():
                    self._security_scope_started = True
            except Exception:
                pass
        ospath = urifile.uristring_to_ospath(interface.uristring)
        if ospath is None:
            from urllib.parse import urlparse, unquote
            pr = urlparse(interface.uristring)
            ospath = unquote(pr.path)
        self.stream = _coordinated_open(self._nsurl, ospath, "rb", 0)

    def read(self, maxsize):
        return self.stream.read(maxsize)

    def readinto(self, bytesobj):
        return self.stream.readinto(bytesobj)

    def readall(self):
        return self.stream.readall()

    def close(self):
        if self._security_scope_started and self._nsurl is not None:
            try:
                self._nsurl.stopAccessingSecurityScopedResource()
            except Exception:
                pass
            self._security_scope_started = False
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


def _coordinated_open(nsurl, path, mode, buffering=0):
    if nsurl is None:
        return open(path, mode, buffering=buffering)
    try:
        coordinator = NSFileCoordinator.alloc().init()
        result = [None]

        def accessor(coordinated_url):
            p = str(coordinated_url.path()) if coordinated_url.path() else path
            result[0] = open(p, mode, buffering=buffering)

        block = Block(accessor, argtypes=['@'], restype='v')

        if 'r' in mode and '+' not in mode:
            coordinator.coordinateReadingItemAtURL_options_error_byAccessor_(
                nsurl, 0, None, block
            )
        else:
            coordinator.coordinateWritingItemAtURL_options_error_byAccessor_(
                nsurl, 0, None, block
            )

        return result[0]
    except Exception:
        return open(path, mode, buffering=buffering)


def _find_parent_nsurl(uristring):
    child_path_str = urifile.uristring_to_ospath(uristring)
    if child_path_str is None:
        return None
    child_path = Path(child_path_str)
    for parent_uristring, parent_url in list(_security_scoped_urls.items()):
        parent_path_str = urifile.uristring_to_ospath(parent_uristring)
        if parent_path_str is None:
            continue
        parent_path = Path(parent_path_str)
        try:
            relative = str(child_path.relative_to(parent_path))
            child_url = parent_url.URLByAppendingPathComponent_(relative)
            if child_url is not None:
                _security_scoped_urls[uristring] = child_url
                return child_url
        except ValueError:
            continue
    return None
