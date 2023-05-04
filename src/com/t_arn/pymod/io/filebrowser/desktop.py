import urllib


class FileBrowserImpl:
    
    def __init__(self, interface):
        self.interface = interface
    # __init__
    
    async def open_file_dialog(self, title, initial_uri, file_types, multiselect):
        selected_uri = []
        initial_path = self.uristring_to_path(uristring)
        result = await self.interface.app.main_window.open_file_dialog (
            title, initial_directory=initial_path, 
            file_types=file_types, multiselect=multiselect, on_result=None)
        if result is None:
            return selected_uri
        if multiselect is False:
            selected_uri.append(self.path_to_uristring(result))
        else:
            for fname in result:
                selected_uri.append(self.path_to_uristring(fname))
        return selected_uri
    # open_file_dialog

    async def save_file_dialog(title, suggested_filename, initial_uri, file_types)
        selected_uri = None
        try:
            result = await save_file_dialog(title, suggested_filename, file_types)
        except ValueError as ex:
            selected_uri = None
            self.interface.log(str(ex))
        finally:
            return selected_uri
    # save_file_dialog
    
    def uri_infos(self, uristring):
        infos = {}
        cursor = None
        if uristring is None:
            return infos
        try:
            uri = Uri.parse(uristring)
            resolver = self.interface.app._impl.native.getContentResolver()
            cursor = resolver.query(uri, None, None, None, None, None)
            if cursor is not None and cursor.moveToFirst():
                index = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME)
                infos["display_name"] = cursor.getString(index)
                n = cursor.getString(index)
                index = cursor.getColumnIndex(OpenableColumns.SIZE)
                size = cursor.getString(index)
                if size is None:
                    size = -1
                infos["size"] = size
                infos["type"] = resolver.getType(uri)
        except BaseException as ex:
            self.interface.log(str(ex))
        finally:
            if cursor is not None:
                cursor.close()
            return infos
    # uri_infos
    
    def path_to_uristring(self, path):
        result = None
        if type(uristring) is not str:
            return result
        result = "file://"+urllib.parse.quote_plus(path)
        return result
    # path_to_uristring
        
    def uristring_to_path(self, uristring):
        result = None
        if type(uristring) is not str or not uristring.startswith("file://"):
            return result
        result = urllib.parse.unquote_plus(uristring)
        return result[7:]
    # uristring_to_path
    
# FileBrowserImpl
