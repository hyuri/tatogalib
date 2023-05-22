import mimetypes
from pathlib import Path
import ..urifile

class UriFileBrowserImpl:
    
    def __init__(self, interface):
        self.interface = interface
    # __init__
    
    async def open_file_dialog(self, title, initial_uri, file_types, multiselect):
        selected_uri = []
        initial_path = urifile.uristring_to_path(initial_uri)
        result = await self.interface.app.main_window.open_file_dialog (
            title, initial_directory=initial_path, 
            file_types=file_types, multiselect=multiselect, on_result=None)
        if result is None:
            return selected_uri
        if multiselect is False:
            result = str(result)  # handle bug in toga open_file_dialog
            selected_uri.append(urifile.path_to_uristring(result))
        else:
            for fname in result:
                fname = str(fname)  # handle bug in toga open_file_dialog
                selected_uri.append(urifile.path_to_uristring(fname))
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
            path = Path(urifile.uristring_to_path(uristring))
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
    
# UriFileBrowserImpl
