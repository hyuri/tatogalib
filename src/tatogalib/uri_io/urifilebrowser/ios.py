import mimetypes
from pathlib import Path
import toga
from .. import urifile


class UriFileBrowserImpl:
    def __init__(self, interface):
        self.interface = interface
        self.app = toga.App.app

    def uri_infos(self, uristring):
        infos = {}
        if uristring is None:
            return infos
        try:
            path = Path(urifile.uristring_to_ospath(uristring))
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

    async def open_file_dialog(self, title, initial_uri, file_types, multiselect):
        selected_uri = []
        initial_path = urifile.uristring_to_ospath(initial_uri)
        result = await self.app.main_window.open_file_dialog(
            title,
            initial_directory=initial_path,
            file_types=file_types,
            multiple_select=multiselect,
            on_result=None,
        )
        if result is None:
            return selected_uri
        if multiselect is False:
            result = str(result)
            selected_uri.append(urifile.ospath_to_uristring(result))
        else:
            for fname in result:
                fname = str(fname)
                selected_uri.append(urifile.ospath_to_uristring(fname))
        return selected_uri

    async def save_file_dialog(self, title, suggested_filename, file_types):
        selected_uri = None
        try:
            selected_uri = await self.app.main_window.save_file_dialog(
                title, suggested_filename, file_types=file_types
            )
            selected_uri = urifile.ospath_to_uristring(str(selected_uri))
        except ValueError as ex:
            selected_uri = None
            self.interface.log(str(ex))
        finally:
            return selected_uri

    async def select_folder_dialog(self, title, initial_uri=None):
        selected_uri = None
        try:
            initial_path = urifile.uristring_to_ospath(initial_uri)
            selected_uri = await self.app.main_window.select_folder_dialog(
                title, initial_path
            )
            if selected_uri is not None:
                selected_uri = urifile.ospath_to_uristring(str(selected_uri))
        except ValueError as ex:
            selected_uri = None
            self.interface.log(str(ex))
        finally:
            return selected_uri
