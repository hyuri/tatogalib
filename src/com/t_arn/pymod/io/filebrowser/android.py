# import Android classes
from android.app import Activity
from android.content import Intent
from android.net import Uri

class FileBrowser:
    
    def __init__(self, app, userapp):
        self.app = app
        self.userapp = userapp  # just for debugging, will be removed later
    # __init__
    
    async def open_file_dialog(self, title, initial_uri=None, file_mime_types=None, multiselect=False):
        """
        Opens an open file dialog and returns the chosen files as list of content URI-strings. 
        Returns [] if nothing has been chosen
          
        :param str title: The title is ignored on Android 
        :param initial_uri: The initial location shown in the file chooser. Must be a content URI, e.g. 
            "content://com.android.externalstorage.documents/document/primary%3ADownload%2FTest-dir"
        :type initial_uri: str or None 
        :param file_mime_types: The file types allowed to select. Must be MIME types, e.g. 
            ["application/pdf","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"].
        :type file_mime_types: list[str] or None 
        :param bool multiselect: If True, then several files can be selected
        
        :returns: the URI-strings of the selected files
        :rtype: list[str]
        """
        intent = Intent(Intent.ACTION_OPEN_DOCUMENT)   # Intent.ACTION_GET_CONTENT
        intent.setType("*/*")
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        if initial_uri is not None and len(initial_uri) > 0: 
            intent.putExtra("android.provider.extra.INITIAL_URI", Uri.parse(initial_uri)) 
        if file_mime_types is not None and len(file_mime_types) > 0: 
            intent.putExtra(Intent.EXTRA_MIME_TYPES, file_mime_types) 
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, multiselect) 
        selected_uri = []
        result = await self.app._impl.intent_result(intent) 
        # result = await self.app._impl.native.startActivityForResult(intent, 1234) 
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
        :param initial_uri: The initial location shown in the file chooser. Must be a content URI, e.g. 
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
        result = await self.app._impl.intent_result(intent) 
        if result["resultCode"] == Activity.RESULT_OK: 
            if result["resultData"] is not None: 
                data = result["resultData"].getData() 
                if data is not None:
                    selected_uri = data.toString()
        return selected_uri
    # save_file_dialog

# FileBrowser
