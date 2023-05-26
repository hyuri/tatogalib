from android.app import Activity
from android.content import Intent
from android.net import Uri
from android.database import Cursor
from android.provider import OpenableColumns
import java
from java.lang import String
import mimetypes
import toga


class UriFileBrowserImpl:
    
    def __init__(self, interface):
        self.interface = interface
        self.app = toga.App.app
        if not mimetypes.inited:
            mimetypes.init()
            mimetypes.add_type("application/vnd.openxmlformats-officedocument.wordprocessingml.document", ".docx", strict=False)
            mimetypes.add_type("application/vnd.ms-word.document.macroEnabled.12", ".docm", strict=False)
            mimetypes.add_type("application/vnd.ms-excel.sheet.macroEnabled.12", ".xlsm", strict=False)
            mimetypes.add_type("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ".xlsx", strict=False)
            mimetypes.add_type("application/vnd.oasis.opendocument.text", ".odt", strict=False)
            mimetypes.add_type("application/vnd.oasis.opendocument.spreadsheet", ".ods", strict=False)
    # __init__
    
    async def open_file_dialog(self, title, initial_uri, file_types, multiselect):
        extensions = file_types
        ftypes = []
        for ext in extensions:
            (mime_type, encoding) = mimetypes.guess_type("filename."+ext, strict=False)
            if mime_type is None:
                self.interface.log(f"Can't guess MIME type for {ext}")
                ftypes = None
                break
            ftypes.append(mime_type)
        if ftypes is not None:
            file_types = java.jarray(String)(ftypes)
        else:
            file_types = None
        intent = Intent(Intent.ACTION_OPEN_DOCUMENT)
        intent.setType("*/*")
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        if initial_uri is not None and len(initial_uri) > 0: 
            intent.putExtra("android.provider.extra.INITIAL_URI", Uri.parse(initial_uri))
        if file_types is not None and len(file_types) > 0: 
            intent.putExtra(Intent.EXTRA_MIME_TYPES, file_types) 
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

    async def save_file_dialog(self, title, suggested_filename, file_types):
        extensions = file_types
        ftypes = []
        for ext in extensions:
            (mime_type, encoding) = mimetypes.guess_type("filename."+ext, strict=False)
            if mime_type is None:
                self.interface.log(f"Can't guess MIME type for {ext}")
                ftypes = None
                break
            ftypes.append(mime_type)
        if ftypes is not None:
            file_types = java.jarray(String)(ftypes)
        else:
            file_types = None
        intent = Intent(Intent.ACTION_CREATE_DOCUMENT)
        intent.setType("*/*")
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        if suggested_filename is not None and len(suggested_filename) > 0: 
            intent.putExtra(Intent.EXTRA_TITLE, suggested_filename) 
        if file_types is not None and len(file_types) > 0: 
            intent.putExtra(Intent.EXTRA_MIME_TYPES, file_types) 
        selected_uri = None
        result = await self.app._impl.intent_result(Intent.createChooser(intent, title))
        if result["resultCode"] == Activity.RESULT_OK: 
            if result["resultData"] is not None: 
                data = result["resultData"].getData() 
                if data is not None:
                    selected_uri = data.toString()
        return selected_uri
    # save_file_dialog

    async def select_folder_dialog(self, title, initial_uri=None): 
        intent = Intent(Intent.ACTION_OPEN_DOCUMENT_TREE)
        if initial_uri is not None and len(initial_uri) > 0: 
            intent.putExtra("android.provider.extra.INITIAL_URI", Uri.parse(initial_uri))
        selected_uri = None
        result = await self.app._impl.intent_result(Intent.createChooser(intent, title))
        if result["resultCode"] == Activity.RESULT_OK: 
            if result["resultData"] is not None: 
                data = result["resultData"].getData() 
                if data is not None:
                    selected_uri = data.toString()
        return selected_uri
    # select_folder_dialog
    
# UriFileBrowserImpl


version = "1.0.0"
version_date = "2023-05-23 - 2023-05-23"
