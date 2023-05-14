import toga

class UriFile:
    
    def __init__(self, app, uristring, fnLog=None):
        """
        Creates a UriFile
        
        :param toga.App app: The current App object
        :param str uristring: A URI-string representing this this UriFile object
        :param callable fnLog: The callable which is called from the log method
            It expects a string parameter
        """
        self.app = app
        self.uristring = uristring
        self.fnLog = fnLog  # for logging to user code
        if toga.platform.current_platform == "android":
            from .android import UriFileImpl
        if toga.platform.current_platform == "windows":
            from .desktop import UriFieImpl
        self.impl = UriFileImpl(self)
    # __init__

    @property
    def display_name(self):
        return self.impl.display_name
    # display_name
    
    @property
    def size(self):
        return self.impl.size
    # size
    
    @property
    def mime_type(self):
        return self.impl.mime_type
    # mime_type
# UriFile
