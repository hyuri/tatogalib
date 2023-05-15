from android.net import Uri
from androidx.documentfile.provider import DocumentFile


class UriFileImpl:
    
    def __init__(self, interface, is_file=True):
            self.interface = interface
            self.context = interface.app._impl.native
            self.resolver = self.context.getContentResolver()
            uri = Uri.parse(interface.uristring)
            if is_file:
                self.docfile = DocumentFile.fromSingleUri(self.context, uri)
            else:
                self.docfile = DocumentFile.fromTreeUri(self.context, uri)
        # __init__
    
    @property
    def display_name(self):
        return self.docfile.getName()
    # display_name
    
    @property
    def exists(self):
        return self.docfile.exists()
    # exists
    
    @property
    def isdir(self):
        return self.docfile.isDirectory()
    # isdir

    @property
    def isfile(self):
        return self.docfile.isFile()
    # isfilr
    
    @property
    def mime_type(self):
        return self.docfile.getType()
    # mime_type
    
    @property
    def size(self):
        return self.docfile.length()
    # size


# UriFileImpl
