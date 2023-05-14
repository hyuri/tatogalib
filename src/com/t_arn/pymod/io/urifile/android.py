from android.net import Uri
from androidx.documentfile.provider import DocumentFile


class UriFileImpl:
    
    def __init__(self, interface):
            self.interface = interface
            self.context = interface.app._impl.native
            self.resolver = self.context.getContentResolver()
            uri = Uri.parse(interface.uristring)
            self.docfile = DocumentFile.fromSingleUri(self.context, uri)
        # __init__
    
    @property
    def display_name(self):
        return self.docfile.getName()
    # display_name
    
    @property
    def size(self):
        return self.docfile.length()
    # size
    
    @property
    def mime_type(self):
        return self.docfile.getType()
    # mime_type

# UriFileImpl
