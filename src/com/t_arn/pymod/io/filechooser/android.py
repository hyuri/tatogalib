# from java import dynamic_proxy, jboolean, jvoid, Override, static_proxy from java import dynamic_proxy, jboolean, jvoid, Override, static_proxy 

# from rubicon.java import JavaClass
# Uri = JavaClass("android/net/Uri")

from android.content import Intent
from android.net import Uri

class FileChooser:
    
    def __init__(self):
        pass
    # __init__
    
    async def choose_file(self, title, initial_uri=None, file_mime_types=None, multiselect=False):
        """
        Opens a file chooser dialog and returns the chosen file as content URI. 
        Returns None has been selected 
          
        :param str title: The title is ignored on Android 
        :param initial_uri: The initial location shown in the file chooser. Must be a content URI, e.g. 
            "content://com.android.externalstorage.documents/document/primary%3ADownload%2FTest-dir"
        :type initial_uri: str or None 
        :param file_mime_types: The file types allowed to select. Must be MIME types, e.g. 
            ["application/pdf","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"].
        :type file_mime_types: list[str] or None 
        :param bool multiselect: If True, then several files can be selected
        
        :returns: the URI(s) of the selected file(s)
        :rtype: str, list[str] or None
        """
        intent = Intent(Intent.ACTION_OPEN_DOCUMENT)
        intent.addCategory(Intent.CATEGORY_OPENABLE) 
        intent.setType("*/*") 
        if initial_uri is not None and initial_uri != '': 
            intent.putExtra("android.provider.extra.INITIAL_URI", Uri.parse(initial_uri)) 
        if file_mime_types is not None and len(file_mime_types) > 0: 
            intent.putExtra(Intent.EXTRA_MIME_TYPES, file_mime_types) 
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, multiselect) 
        selected_uri = None 
        result = await self.app.intent_result(intent) 
        if result["resultCode"] == Activity.RESULT_OK: 
            if result["resultData"] is not None: 
                selected_uri = result["resultData"].getData() 
                if multiselect: 
                    if selected_uri is None: 
                        # when the user selects more than 1 file, getData() will be None. Instead, getClipData() will 
                        # contain the list of chosen files 
                        selected_uri = [] 
                        clip_data = result["resultData"].getClipData() 
                        if clip_data is not None:  # just to be sure there will never be a null reference exception... 
                            for i in range(0, clip_data.getItemCount()): 
                                selected_uri.append(str(clip_data.getItemAt(i).getUri())) 
                        else: 
                            selected_uri = [str(selected_uri)]
                return selected_uri
    # choose_file
# FileChooser
