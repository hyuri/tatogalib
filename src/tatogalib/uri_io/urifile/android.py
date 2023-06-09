from android.net import Uri
from android.content import ContentValues, Intent
from android.provider import DocumentsContract
from androidx.documentfile.provider import DocumentFile
import java
import toga


class UriFileImpl:
    def __init__(self, interface):
        self.interface = interface
        self.context = toga.App.app._impl.native
        self.resolver = self.context.getContentResolver()
        self.uri = Uri.parse(interface.uristring)
        if "/document/" in interface.uristring:
            if "/tree/" in interface.uristring:
                # to do: create tree uri and call fromTreeUri
                # We could use DocumentsContract.buildTreeDocumentUri
                # but we do not have rights there even when we have
                # rights to the parent folder
                self.docfile = DocumentFile.fromSingleUri(self.context, self.uri)
            else:
                self.docfile = DocumentFile.fromSingleUri(self.context, self.uri)
        else:
            self.docfile = DocumentFile.fromTreeUri(self.context, self.uri)

    # __init__

    def delete(self):
        return self.docfile.delete()

    # delete

    def get_name(self):
        return self.docfile.getName()

    # get_name

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
            updateValues.put(
                DocumentsContract.Document.COLUMN_LAST_MODIFIED, java.jlong(unixtime)
            )
            self.interface.log("calling update")
            updated = self.resolver.update(self.uri, updateValues, None, None)
        except Exception as ex:
            updated = 0
            self.interface.log(str(ex))
        finally:
            return updated == 1

    # set_lastmodified

    def listdir(self):
        result = []
        children = self.docfile.listFiles()
        for df in children:
            uristring = df.getUri().toString()
            """
            This returns the correct treeUri of subfolders, but we do not have rights there
            if df.isDirectory():
                childAsRootUri = DocumentsContract.buildTreeDocumentUri(
                    self.uri.getAuthority(), DocumentsContract.getDocumentId(df.getUri())
                )
                uristring = childAsRootUri.toString()
                self.interface.log(uristring)
            """
            result.append(uristring)
        return result

    # listdir

    def get_mime_type(self):
        return self.docfile.getType()

    # get_mime_type

    def request_persistent_access(self):
        flags = 0
        flags = flags | (
            Intent.FLAG_GRANT_READ_URI_PERMISSION
            | Intent.FLAG_GRANT_WRITE_URI_PERMISSION
        )
        self.resolver.takePersistableUriPermission(self.uri, flags)

    # request_persistent_access

    def get_size(self):
        return self.docfile.length()

    # get_size


# UriFileImpl


version = "0.6.0"
version_date = "2023-05-23 - 2023-06-02"
