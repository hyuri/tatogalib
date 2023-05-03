from android.app import Activity
from android.content import Intent
from android.net import Uri
from android.database import Cursor
from android.provider import OpenableColumns


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
    
    async def open_file_dialog(self, title, initial_uri=None, file_mime_types=None, multiselect=False):
        """
        Opens an open file dialog and returns the chosen files as list of content URI-strings. 
        Returns [] if nothing has been chosen
          
        :param str title: The title is ignored on Android 
        :param initial_uri: The initial location shown in the file chooser. Must be a content URI-string, e.g. 
            "content://com.android.externalstorage.documents/document/primary%3ADownload%2FTest-dir"
        :type initial_uri: str or None 
        :param file_mime_types: The file types allowed to select. Must be MIME types, e.g. 
            ["application/pdf","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"].
        :type file_mime_types: list[str] or None 
        :param bool multiselect: If True, then several files can be selected
        
        :returns: the URI-strings of the selected files
        :rtype: list[str]
        """
        intent = Intent(Intent.ACTION_OPEN_DOCUMENT)
        intent.setType("*/*")
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        if initial_uri is not None and len(initial_uri) > 0: 
            intent.putExtra("android.provider.extra.INITIAL_URI", Uri.parse(initial_uri)) 
        if file_mime_types is not None and len(file_mime_types) > 0: 
            intent.putExtra(Intent.EXTRA_MIME_TYPES, file_mime_types) 
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, multiselect) 
        selected_uri = []
        result = await self.app._impl.intent_result(Intent.createChooser(intent, title))
        if result["resultCode"] == Activity.RESULT_OK: 
            if result["resultData"] is not None: 
                data = result["resultData"].getData() 
                if data is None:
                    if multiselect:
                        # when the user selects more than 1 file, getData() will be None. Instead, getClipData() will 
                        # contain the list of chosen files 
                        clip_data = result["resultData"].getClipData() 
                        if clip_data is not None:  # just to be sure there will never be a null reference exception... 
                            for i in range(0, clip_data.getItemCount()): 
                                selected_uri.append(clip_data.getItemAt(i).getUri().toString())
                else:
                    selected_uri = [data.toString()]
        return selected_uri
    # open_file_dialog

    async def save_file_dialog(self, title, initial_uri=None, file_mime_types=None):
        """
        Opens a file save dialog and returns the chosen file as a content URI-string. 
        Returns None if nothing has been chosen
          
        :param str title: The title is ignored on Android 
        :param initial_uri: The initial location shown in the file chooser. Must be a content URI-string, e.g. 
            "content://com.android.externalstorage.documents/document/primary%3ADownload%2FTest-dir"
        :type initial_uri: str or None 
        :param file_mime_types: The file types allowed to select. Must be MIME types, e.g. 
            ["application/pdf","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"].
        :type file_mime_types: list[str] or None 
        
        :returns: the URI-string of the selected file or None
        :rtype: str or None
        """
        intent = Intent(Intent.ACTION_CREATE_DOCUMENT)
        intent.setType("*/*")
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        if initial_uri is not None and len(initial_uri) > 0: 
            intent.putExtra("android.provider.extra.INITIAL_URI", Uri.parse(initial_uri)) 
        if file_mime_types is not None and len(file_mime_types) > 0: 
            intent.putExtra(Intent.EXTRA_MIME_TYPES, file_mime_types) 
        selected_uri = None
        result = await self.app._impl.intent_result(Intent.createChooser(intent, title))
        if result["resultCode"] == Activity.RESULT_OK: 
            if result["resultData"] is not None: 
                data = result["resultData"].getData() 
                if data is not None:
                    selected_uri = data.toString()
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
# FileBrowser
