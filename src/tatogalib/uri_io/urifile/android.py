from android.net import Uri
from android.content import ContentValues, Intent
from android.provider import DocumentsContract
from androidx.documentfile.provider import DocumentFile
import java
import mimetypes
from pathlib import Path
from ... import system
import toga
from urllib.parse import urlparse, quote, unquote


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
            # docUri = DocumentsContract.buildDocumentUriUsingTree(self.uri,
            #     DocumentsContract.getTreeDocumentId(self.uri))
            # self.docfile = DocumentFile.fromTreeUri(self.context, docUri)
    # __init__

    def create_file(self, child_name):
        (mimetype, encoding) = mimetypes.guess_type(str(child_name), strict=False)
        if mimetype is None:
            mimetype = "application/octet-stream"
        child = self.docfile.createFile(mimetype, child_name)
        return child.getUri().toString()
    # create_file

    def delete(self):
        return self.docfile.delete()
    # delete

    def exists(self):
        return self.docfile.exists()
    # exists

    def find(self, child_name):
        child = self.docfile.findFile(child_name)
        if child is None:
            return None
        return child.getUri().toString()
    # find

    def from_path(path):
        from . import UriFile
        urifile = None
        p = str(path)
        roots = system.get_file_roots()
        if p.startswith(roots[0]):
            uristring = "content://com.android.externalstorage.documents/document/primary%3A"
            uristring += quote(p[len(roots[0])+1:], safe="!")
            urifile = UriFile(uristring)
        else:
            uristring = "content://com.android.externalstorage.documents/document/"
            for root in roots:
                if p.startswith(root):
                    idx = root.rfind("/")
                    if idx != -1:
                        uristring += quote(root[idx+1:]) + "%3A"
                        uristring += quote(p[len(root)+1:], safe="!")
                        urifile = UriFile(uristring)
        return urifile
    # from_path

    def get_lastmodified(self):
        return self.docfile.lastModified()
    # get_lastmodified

    def get_mime_type(self):
        return self.docfile.getType()
    # get_mime_type

    def get_name(self):
        return self.docfile.getName()
    # get_name

    def get_path(self):
        path = None
        roots = system.get_file_roots()
        if self.is_externalstorage_document():
            pr = urlparse(self.interface.uristring)
            praefix = "/document/primary%3A"
            if pr.path.startswith(praefix):
                path = Path(roots[0]) / unquote(pr.path[len(praefix):])
                print(str(path))
            else:
                for root in roots:
                    idx = root.rfind("/")
                    fsid = root[idx+1:]
                    praefix = f"/document/{fsid}%3A"
                    print(f"präfix={praefix}")
                    print(f"pr.path={pr.path}")
                    if pr.path.startswith(praefix):
                        path = Path(root) / unquote(pr.path[len(praefix):])
        return path
    # get_path

    def get_persisted_permissions():
        context = toga.App.app._impl.native
        resolver = context.getContentResolver()
        tree_permissions = []
        permissions = resolver.getPersistedUriPermissions()
        for i in range (0, permissions.size()):
            p = {}
            p["uri"] = permissions.get(i).getUri().toString()
            p["is_read_permission"] = permissions.get(i).isReadPermission()
            p["is_write_permission"] = permissions.get(i).isWritePermission()
            tree_permissions.append(p)
        return tree_permissions
    # get_persisted_permissions
 
    def get_size(self):
        return self.docfile.length()
    # get_size

    def isdir(self):
        return self.docfile.isDirectory()
    # isdir

    def isfile(self):
        return self.docfile.isFile()
    # isfile

    def is_downloads_document(self):
        pr = urlparse(self.interface.uristring)
        return pr.scheme == "content" and pr.netloc ==  "com.android.providers.downloads.documents"
    # is_downloads_document

    def is_externalstorage_document(self):
        pr = urlparse(self.interface.uristring)
        return pr.scheme == "content" and pr.netloc ==  "com.android.externalstorage.documents"
    # is_externalstorage_document

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

    def request_persistent_access(self):
        flags = 0
        flags = flags | (
            Intent.FLAG_GRANT_READ_URI_PERMISSION
            | Intent.FLAG_GRANT_WRITE_URI_PERMISSION
        )
        self.resolver.takePersistableUriPermission(self.uri, flags)
    # request_persistent_access

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

# UriFileImpl
