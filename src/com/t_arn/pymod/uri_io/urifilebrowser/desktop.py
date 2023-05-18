import mimetypes
import os
from pathlib import Path
from urllib.parse import urlparse, unquote
from urllib.request import url2pathname


class UriFileBrowserImpl:
    
    def __init__(self, interface):
        self.interface = interface
    # __init__
    
    async def open_file_dialog(self, title, initial_uri, file_types, multiselect):
        selected_uri = []
        initial_path = self.uristring_to_path(initial_uri)
        result = await self.interface.app.main_window.open_file_dialog (
            title, initial_directory=initial_path, 
            file_types=file_types, multiselect=multiselect, on_result=None)
        if result is None:
            return selected_uri
        if multiselect is False:
            result = str(result)  # handle bug in toga open_file_dialog
            selected_uri.append(self.path_to_uristring(result))
        else:
            for fname in result:
                fname = str(fname)  # handle bug in toga open_file_dialog
                selected_uri.append(self.path_to_uristring(fname))
        return selected_uri
    # open_file_dialog

    async def save_file_dialog(title, suggested_filename, initial_uri, file_types): 
        selected_uri = None
        try:
            selected_uri = await self.interface.app.main_window.save_file_dialog(
                title, suggested_filename, file_types=file_types)
        except ValueError as ex:
            selected_uri = None
            self.interface.log(str(ex))
        finally:
            return selected_uri
    # save_file_dialog
    
    def uri_infos(self, uristring):
        infos = {}
        if uristring is None:
            return infos
        try:
            path = Path(self.uristring_to_path(uristring))
            infos["display_name"] = path.name
            infos["size"] = path.stat().st_size
            (mime_type, encoding) = mimetypes.guess_type(uristring, strict=False)
            if mime_type is None:
                self.interface.log(f"Can't guess MIME type for {uristring}")
            infos["type"] = mime_type
        except BaseException as ex:
            self.interface.log(str(ex))
        finally:
            return infos
    # uri_infos
    
    def path_to_uristring(self, path):
        result = None
        if type(path) is not str:
            return result
        result = Path(path).as_uri()
        return result
    # path_to_uristring
        
    def uristring_to_path(self, uristring):
        result = None
        if type(uristring) is not str or not uristring.startswith("file://"):
            return result
        parsed = urlparse(uristring)
        host = "{0}{0}{mnt}{0}".format(os.path.sep, mnt=parsed.netloc)
        return os.path.normpath(
            os.path.join(host, url2pathname(unquote(parsed.path)))
        )
    # uristring_to_path
    
# UriFileBrowserImpl
