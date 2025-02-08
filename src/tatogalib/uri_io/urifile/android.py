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
                self.docfile = DocumentFile.fromSingleUri(self.context, self.uri)
            else:
                self.docfile = DocumentFile.fromSingleUri(self.context, self.uri)
        else:
            self.docfile = DocumentFile.fromTreeUri(self.context, self.uri)

    # __init__

    @staticmethod
    def from_path(path):
        from . import UriFile

        urifile = None
        p = str(path)
        roots = system.get_file_roots()
        if p.startswith(roots[0]):
            uristring = (
                "content://com.android.externalstorage.documents/document/primary%3A"
            )
            uristring += quote(p[len(roots[0]) + 1 :], safe="!")
            urifile = UriFile(uristring)
        else:
            uristring = "content://com.android.externalstorage.documents/document/"
            for root in roots:
                if p.startswith(root):
                    idx = root.rfind("/")
                    if idx != -1:
                        uristring += quote(root[idx + 1 :]) + "%3A"
                        uristring += quote(p[len(root) + 1 :], safe="!")
                        urifile = UriFile(uristring)
        return urifile

    # from_path

    @staticmethod
    def get_persisted_permissions():
        context = toga.App.app._impl.native
        resolver = context.getContentResolver()
        tree_permissions = []
        permissions = resolver.getPersistedUriPermissions()
        for i in range(0, permissions.size()):
            p = {}
            p["uri"] = str(permissions.get(i).getUri())
            p["is_read_permission"] = permissions.get(i).isReadPermission()
            p["is_write_permission"] = permissions.get(i).isWritePermission()
            p["persisted_time"] = permissions.get(i).getPersistedTime()
            tree_permissions.append(p)
        sorted_list = sorted(tree_permissions, key=lambda d: d["persisted_time"])
        return sorted_list

    # get_persisted_permissions

    @staticmethod
    def get_uripath(uristring):
        uripath = None
        idx = uristring.rfind("/document/")
        if idx != -1:
            uripath = uristring[idx + len("/document/") :]
        else:
            idx = uristring.rfind("/tree/")
            if idx != -1:
                uripath = uristring[idx + len("/tree/") :]
        return uripath

    # get_uripath

    @staticmethod
    def is_child(parent_uristring, uristring):
        """
        Checks if doc_uristring is a descendant of parent_uristring.
        Both uristrings can be a tree URI or a document URI

        :param str parent_uristring: The parent folder
        :param str uristring: The file or folder to be checked
        :returns: True or False
        """
        uripath = UriFileImpl.get_uripath(uristring)
        uripath_parent = UriFileImpl.get_uripath(parent_uristring)
        if uripath.startswith(uripath_parent):
            return True
        return False

    # is_child

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

    def get_lastmodified(self):
        return self.docfile.lastModified()

    # get_lastmodified

    def get_mime_type(self):
        return self.docfile.getType()

    # get_mime_type

    def get_name(self):
        return self.docfile.getName()
    
    # get_name
    
    def get_stem(self):
        return Path(self.get_name()).stem
    
    def get_suffix(self):
        return Path(self.get_name()).suffix
    
    def get_parent(self):
        return Path(self.get_name()).parent

    def get_authorized_uristring(self):
        docId = DocumentsContract.getDocumentId(self.docfile.getUri())
        permissions = self.get_persisted_permissions()
        docTreeUri = None
        for p in permissions:
            if self.is_child(p["uri"], self.interface.get_uristring()):
                docTreeUri = DocumentsContract.buildDocumentUriUsingTree(
                    Uri.parse(p["uri"]), docId
                )
                break
        if docTreeUri is not None:
            return docTreeUri.toString()
        else:
            return None

    # get_authorized_uristring

    def get_path(self):
        path = None
        roots = system.get_file_roots()
        if self.is_externalstorage_document():
            pr = urlparse(self.interface.uristring)
            prefix = "/document/primary%3A"
            if pr.path.startswith(prefix):
                path = Path(roots[0]) / unquote(pr.path[len(prefix) :])
                print(str(path))
            else:
                for root in roots:
                    idx = root.rfind("/")
                    fsid = root[idx + 1 :]
                    prefix = f"/document/{fsid}%3A"
                    print(f"prefix={prefix}")
                    print(f"pr.path={pr.path}")
                    if pr.path.startswith(prefix):
                        path = Path(root) / unquote(pr.path[len(prefix) :])
        return path

    # get_path

    def get_size(self):
        return self.docfile.length()

    # get_size

    def is_dir(self):
        return self.docfile.isDirectory()

    # is_dir

    def is_file(self):
        return self.docfile.isFile()

    # is_file

    def is_downloads_document(self):
        pr = urlparse(self.interface.uristring)
        return (
            pr.scheme == "content"
            and pr.netloc == "com.android.providers.downloads.documents"
        )

    # is_downloads_document

    def is_externalstorage_document(self):
        pr = urlparse(self.interface.uristring)
        return (
            pr.scheme == "content"
            and pr.netloc == "com.android.externalstorage.documents"
        )

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

    def release_persistent_access(self, read=True, write=True):
        try:
            flags = 0
            if read:
                flags = flags | Intent.FLAG_GRANT_READ_URI_PERMISSION
            if write:
                flags = flags | Intent.FLAG_GRANT_WRITE_URI_PERMISSION
            self.resolver.releasePersistableUriPermission(self.uri, flags)
        except Exception as ex:
            print(str(ex))
            self.interface.log(str(ex))

    # release_persistent_access

    def request_persistent_access(self, read=True, write=True):
        try:
            flags = 0
            if read:
                flags = flags | Intent.FLAG_GRANT_READ_URI_PERMISSION
            if write:
                flags = flags | Intent.FLAG_GRANT_WRITE_URI_PERMISSION
            self.resolver.takePersistableUriPermission(self.uri, flags)
        except Exception as ex:
            print(str(ex))
            self.interface.log(str(ex))

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
