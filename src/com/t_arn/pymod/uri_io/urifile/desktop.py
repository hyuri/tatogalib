import mimetypes
import os
from pathlib import Path
from .. import urifile


class UriFileImpl:
    
    def __init__(self, interface, is_file=True):
        self.interface = interface
        ospath = urifile.uristring_to_ospath(interface.uristring)
        self.path = Path(ospath)
   # __init__

    def delete(self): 
        if self.isfile():
            try:
                self.path.unlink(missing_ok=True)
            except Exception as ex:
                self.interface.log(str(ex))
        return not self.exists()
    # delete
    
    def get_display_name(self):
        return self.path.name
    # get_display_name
    
    def exists(self):
        return self.path.exists()
    # exists
    
    def isdir(self):
        return self.path.is_dir()
    # isdir

    def isfile(self):
        return self.path.is_file()
    # isfile
    
    def get_lastmodified(self): 
        return int(os.path.getmtime(str(self.path)))
    # get_lastmodified
        
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
    
    def get_mime_type(self):
        (mimetype, encoding) = mimetypes.guess_type(str(self.path), strict=False)
        return mimetype
    # get_mime_type
    
    def get_size(self):
        return self.path.stat().st_size
    # get_size

# UriFileImpl


version = "0.5.0"
version_date = "2023-05-23 - 2023-05-23"
