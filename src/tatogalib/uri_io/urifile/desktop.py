import mimetypes
import os
from pathlib import Path
from .. import urifile


class UriFileImpl:
    def __init__(self, interface):
        self.interface = interface
        ospath = urifile.uristring_to_ospath(interface.uristring)
        self.path = Path(ospath)

    # __init__

    @staticmethod
    def from_path(path):
        from . import UriFile

        uristring = urifile.ospath_to_uristring(str(path))
        if uristring is None:
            return None
        return UriFile(uristring)

    # from_path

    def create_file(self, child_name):
        path = self.path / child_name
        Path.touch(path)
        return urifile.ospath_to_uristring(str(path))

    # create_file

    def delete(self):
        if self.isfile():
            try:
                self.path.unlink(missing_ok=True)
            except Exception as ex:
                self.interface.log(str(ex))
        return not self.exists()

    # delete

    def exists(self):
        return self.path.exists()

    # exists

    def find(self, child_name):
        path = self.path / child_name
        if path.exists():
            return urifile.ospath_to_uristring(str(path))
        return None

    # find

    def get_authorized_uristring(self):
        return self.interface.uristring

    # get_authorized_uristring

    @staticmethod
    def get_persisted_permissions():
        return []

    # get_persisted_permissions

    def get_lastmodified(self):
        return int(os.path.getmtime(str(self.path)))

    # get_lastmodified

    def get_mime_type(self):
        (mimetype, encoding) = mimetypes.guess_type(str(self.path), strict=False)
        return mimetype

    # get_mime_type

    def get_name(self):
        return self.path.name

    # get_name

    def get_path(self):
        return self.path

    # get_path

    def get_size(self):
        return self.path.stat().st_size

    # get_size

    def isdir(self):
        return self.path.is_dir()

    # isdir

    def isfile(self):
        return self.path.is_file()

    # isfile

    def listdir(self):
        result = []
        self.interface.log(str(self.path))
        children = os.listdir(self.path)
        for child in children:
            self.interface.log(str(child))
            uristring = urifile.ospath_to_uristring(str(self.path / child))
            result.append(uristring)
        return result

    # listdir

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

    # set_lastmodified


# UriFileImpl
