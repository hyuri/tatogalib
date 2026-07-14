import mimetypes
import os
from pathlib import Path
from .. import urifile


class UriFileImpl:
    def __init__(self, interface):
        self.interface = interface
        ospath = urifile.uristring_to_ospath(interface.uristring)
        if ospath is None:
            from urllib.parse import urlparse, unquote
            pr = urlparse(interface.uristring)
            ospath = unquote(pr.path)
        self.path = Path(ospath)

    def __str__(self):
        return str(self.path)

    def get_truediv_uristring(self, other):
        from . import UriFile
        parent = self.path
        if isinstance(other, UriFile):
            child = other.path
        elif isinstance(other, str) or isinstance(other, Path):
            child = other
        else:
            raise TypeError(f"Unsupported operand type(s) for /: 'UriFile' and '{type(other).__name__}'")
        return str(parent / child)

    @staticmethod
    def uristring_from_path(path):
        return urifile.ospath_to_uristring(str(path))

    @staticmethod
    def from_path(path):
        from . import UriFile
        uristring = urifile.ospath_to_uristring(str(path))
        if uristring is None:
            return None
        return UriFile(uristring)

    @staticmethod
    def get_persisted_permissions():
        return []

    @staticmethod
    def get_uripath(uristring):
        from urllib.parse import urlparse, unquote
        pr = urlparse(uristring)
        return unquote(pr.path)

    @staticmethod
    def is_child(parent_uristring, uristring):
        parent_path = UriFileImpl.get_uripath(parent_uristring)
        child_path = UriFileImpl.get_uripath(uristring)
        return child_path.startswith(parent_path)

    def create_file(self, child_name):
        path = self.path / child_name
        Path.touch(path)
        return urifile.ospath_to_uristring(str(path))

    def create_dir(self, child_name, replace=False, exists_ok=False):
        path = self.path / child_name
        path.mkdir(exist_ok=exists_ok)
        return urifile.ospath_to_uristring(str(path))

    def unlink(self):
        if self.is_file():
            try:
                self.path.unlink(missing_ok=True)
            except Exception as ex:
                self.interface.log(str(ex))
        return not self.exists()

    def exists(self):
        return self.path.exists()

    def find(self, child_name):
        path = self.path / child_name
        if path.exists():
            return urifile.ospath_to_uristring(str(path))
        return None

    def get_authorized_uristring(self):
        return self.interface.uristring

    def get_lastmodified(self):
        return int(os.path.getmtime(str(self.path)))

    def get_mime_type(self):
        (mimetype, encoding) = mimetypes.guess_type(str(self.path), strict=False)
        return mimetype

    def get_name(self):
        return self.path.name

    def get_stem(self):
        return self.path.stem

    def get_suffix(self):
        return self.path.suffix

    def with_suffix(self, suffix):
        from . import UriFile
        suffixed_path = self.path.with_suffix(suffix)
        return UriFile.from_path(suffixed_path)

    def get_parent(self):
        from . import UriFile
        parent = self.path.parent
        return UriFile.from_path(parent)

    def get_path(self):
        return self.path

    def get_size(self):
        return self.path.stat().st_size

    def is_dir(self):
        return self.path.is_dir()

    def is_file(self):
        return self.path.is_file()

    def listdir(self):
        result = []
        children = os.listdir(self.path)
        for child in children:
            uristring = urifile.ospath_to_uristring(str(self.path / child))
            result.append(uristring)
        return result

    def relative_to(self, other):
        self_path = str(self.path)
        other_path = str(other.path) if hasattr(other, 'path') else str(other._impl.path)
        return Path(self_path).relative_to(other_path)

    def resolve(self, other):
        from . import UriFile
        self_path = str(self.path)
        other_path = str(other.path) if hasattr(other, 'path') else str(other._impl.path)
        resolved = (Path(self_path) / other_path).resolve()
        return UriFile.from_path(resolved)

    def set_lastmodified(self, unixtime):
        try:
            atime = os.path.getatime(str(self.path))
            os.utime(str(self.path), times=(atime, unixtime))
            updated = 1
        except Exception as ex:
            updated = 0
            self.interface.log(str(ex))
        finally:
            return updated == 1

    def release_persistent_access(self, read=True, write=True):
        pass

    def request_persistent_access(self, read=True, write=True):
        pass
