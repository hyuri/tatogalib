import urllib


class FileBrowser:
    
    def __init__(self, app, fnLog=None):
        """
        Creates a FileBrowser
        
        :param toga.App app: The current App object
        :param callable fnLog: The callable which is called from the log method
            It expects a string parameter
        """
        self.app = app
        self.fnLog = fnLog  # for logging to user code
    # __init__
    
    async def open_file_dialog(self, title, initial_uri=None, file_types=None, multiselect=False):
        """
        Opens an open file dialog and returns the chosen files as list of file URI-strings. 
        Returns [] if nothing has been chosen
          
        :param str title: The title of the chooser dialog
        :param initial_uri: The initial location shown in the file chooser. Must be a file URI-string, e.g. 
            "file://C:/Program%20Files/Microsoft"
        :type initial_uri: str or None 
        :param file_types: The file types allowed to select. Must be file extensions e.g. 
            ["docx", "pdf"].
        :type file_types: list[str] or None 
        :param bool multiselect: If True, then several files can be selected
        
        :returns: the URI-strings of the selected files
        :rtype: list[str]
        """
        selected_uri = []
        initial_path = self.uristring_to_path(uristring)
        result = await self.app.main_window.open_file_dialog (title, initial_directory=initial_path, 
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

    async def save_file_dialog(self, title, initial_uri=None, file_types=None):
        """
        Opens a file save dialog and returns the chosen file as a content URI-string. 
        Returns None if nothing has been chosen
          
        :param str title: The title is ignored on Android 
        :param initial_uri: The initial location shown in the file chooser. Must be a file URI-string, e.g. 
            "file://C:/Program%20Files/Microsoft"
        :type initial_uri: str or None 
        :param file_types: The file types allowed to select. Must be file extensions e.g. 
            ["docx", "pdf"].
        :type file_types: list[str] or None 
        
        :returns: the URI-string of the selected file or None
        :rtype: str or None
        """
        selected_uri = None
        try:
            
        except ValueError as ex:
            selected_uri = None
            self.fnLog(str(ex))
        finally:
            return selected_uri
    # save_file_dialog
    
    def uri_infos(self, uristring):
        """
        Get name, size and type of the file referenced by the URI-string
        
        :param str uristring: The URI-string
        
        :returns: Dictionary with keys "display_name", "size" and "type"
            It is empty on error
        """
        infos = {}
        cursor = None
        if uristring is None:
            return infos
        try:
            uri = Uri.parse(uristring)
            resolver = self.app._impl.native.getContentResolver()
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
            self.fnLog(str(ex))
        finally:
            if cursor is not None:
                cursor.close()
            return infos
    # uri_infos
    
    def log(self, message):
        """
        Logs a message to the user code if fnLog was passed to the constructor
        
        :param str message: The message to be logged
        """
        if self.fnLog is not None:
            self.fnLog(message)
    # log
    
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
# FileBrowser
