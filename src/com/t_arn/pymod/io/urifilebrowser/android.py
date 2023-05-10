from android.app import Activity
from android.content import Intent
from android.net import Uri
from android.database import Cursor
from android.provider import OpenableColumns
import java
from java.lang import String
import mimetypes


class UriFileBrowserImpl:
    
    def __init__(self, interface):
        self.interface = interface
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
        result = await self.interface.app._impl.intent_result(Intent.createChooser(intent, title))
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

    async def save_file_dialog(self, title, suggested_filename, initial_uri, file_types):
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
        if initial_uri is not None and len(initial_uri) > 0: 
            intent.putExtra("android.provider.extra.INITIAL_URI", Uri.parse(initial_uri)) 
        if file_types is not None and len(file_types) > 0: 
            intent.putExtra(Intent.EXTRA_MIME_TYPES, file_types) 
        selected_uri = None
        result = await self.interface.app._impl.intent_result(Intent.createChooser(intent, title))
        if result["resultCode"] == Activity.RESULT_OK: 
            if result["resultData"] is not None: 
                data = result["resultData"].getData() 
                if data is not None:
                    selected_uri = data.toString()
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
    
# UriFileBrowserImpl
