from android.net import Uri
from android.content import ContentValues
from android.provider import DocumentsContract
from androidx.documentfile.provider import DocumentFile
import java
import toga

class UriFileImpl:
    
    def __init__(self, interface, is_file=True):
            self.interface = interface
            
            self.context = toga.App.app._impl.native
            self.resolver = self.context.getContentResolver()
            self.uri = Uri.parse(interface.uristring)
            if is_file:
                self.docfile = DocumentFile.fromSingleUri(self.context, self.uri)
            else:
                self.docfile = DocumentFile.fromTreeUri(self.context, self.uri)
        # __init__
        
    def delete(self): 
        return self.docfile.delete()
    # delete
    
    def get_display_name(self):
        return self.docfile.getName()
    # get_display_name
    
    def exists(self):
        return self.docfile.exists()
    # exists
    
    def isdir(self):
        return self.docfile.isDirectory()
    # isdir

    def isfile(self):
        return self.docfile.isFile()
    # isfile
    
    def get_lastmodified(self): 
        return self.docfile.lastModified()
    # get_lastmodified
        
    def set_lastmodified(self, unixtime):
        # not working, always results in "Update not supported" exception
        # https://stackoverflow.com/questions/35744654/storage-access-framework-set-last-modified-date-of-local-documentfil
        try:
            updateValues = ContentValues()
            updateValues.put(DocumentsContract.Document.COLUMN_LAST_MODIFIED, java.jlong(unixtime))
            self.interface.log("calling update")
            updated = self.resolver.update(self.uri, updateValues, None, None)
        except Exception as ex:
            updated = 0
            self.interface.log(str(ex))
        finally:
            return updated == 1
    # set_lastmodified
    
    def get_mime_type(self):
        return self.docfile.getType()
    # get_mime_type
    
    def get_size(self):
        return self.docfile.length()
    # get_size

# UriFileImpl


version = "0.5.0"
version_date = "2023-05-23 - 2023-05-23"
