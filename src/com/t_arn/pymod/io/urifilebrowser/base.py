import toga

class UriFileBrowser:
    
    def __init__(self, app, fnLog=None):
        """
        Creates a UriFileBrowser
        
        :param toga.App app: The current App object
        :param callable fnLog: The callable which is called from the log method
            It expects a string parameter
        """
        self.app = app
        self.fnLog = fnLog  # for logging to user code
        if toga.platform.current_platform == "android":
            from .android import UriFileBrowserImpl
        if toga.platform.current_platform == "windows":
            from .desktop import UriFileBrowserImpl
        self.impl = UriFileBrowserImpl(self)
    # __init__
    
    async def open_file_dialog(self, title, initial_uri=None, file_types=None, multiselect=False):
        """
        Opens an open file dialog and returns the chosen files as list of URI-strings. 
        Returns [] if nothing has been chosen
          
        :param str title: The title is ignored on Android 
        :param initial_uri: The initial location shown in the file chooser. 
            On Android, this must be a content URI-string, e.g. 
            "content://com.android.externalstorage.documents/document/primary%3ADownload%2FTest-dir"
            On desktops, it must be file URI-strings, e.g.
            "file://C:/Program%20Files"
        :type initial_uri: str or None 
        :param file_types: The file types allowed to select. Must be file extensions e.g. 
            ["doc", "pdf"].
        :type file_types: list[str] or None 
        :param bool multiselect: If True, then several files can be selected
        
        :returns: the URI-strings of the selected files
        :rtype: list[str]
        """
        result = await self.impl.open_file_dialog(title, initial_uri, file_types, multiselect)
        return result
    # open_file_dialog

    async def save_file_dialog(self, title, suggested_filename, initial_uri=None, file_types=None):
        """
        Opens a file save dialog and returns the chosen file as a URI-string. 
        Returns None if nothing has been chosen
          
        :param str title: The title for the dialog
            On Android, this is ignored
        :param str suggested_filename: The filename to suggest
        :param initial_uri: The initial location shown in the file chooser. 
            On Android, this must be a content URI-string, e.g. 
            "content://com.android.externalstorage.documents/document/primary%3ADownload%2FTest-dir"
            On desktops, it must be file URI-strings, e.g.
            "file://C:/Program%20Files"
        :type initial_uri: str or None 
        :param file_types: The file types allowed to select. Must be file extensions e.g. 
            ["doc", "pdf"].
        :type file_types: list[str] or None 
        
        :returns: the URI-string of the selected file or None
        :rtype: str or None
        """
        result = await self.impl.save_file_dialog(title, suggested_filename, initial_uri, file_types)
        return result
    # save_file_dialog
    
    def uri_infos(self, uristring):
        """
        Get name, size and type of the file referenced by the URI-string
        
        :param str uristring: The URI-string
        
        :returns: Dictionary with keys "display_name", "size" and "type"
            It is empty on error
        """
        return self.impl.uri_infos(uristring)
    # uri_infos
    
    def log(self, message):
        """
        Logs a message to the user code if fnLog was passed to the constructor
        
        :param str message: The message to be logged
        """
        if self.fnLog is not None:
            self.fnLog(message)
    # log
    
# UriFileBrowser
