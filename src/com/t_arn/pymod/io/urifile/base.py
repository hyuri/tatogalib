import toga
from ..uriinputstream import UriInputStream
from ..urioutputstream import UriOutputStream

class UriFile:
    
    def __init__(self, app, uristring, is_file=True, fnLog=None):
        """
        Creates a UriFile
        
        :param toga.App app: The current App object
        :param str uristring: A URI-string representing this this UriFile object
        :param boolean is_file: True when uristring represents a file, False for a folder
        :param callable fnLog: The callable which is called from the log method
            It expects a string parameter
        """
        self.app = app
        self.uristring = uristring
        self.fnLog = fnLog  # for logging to user code
        if toga.platform.current_platform == "android":
            from .android import UriFileImpl
        if toga.platform.current_platform == "windows":
            from .desktop import UriFieImpl
        self.impl = UriFileImpl(self, is_file)
    # __init__

    @property
    def display_name(self):
        return self.impl.display_name
    # display_name
    
    @property
    def exists(self):
        return self.impl.exists
    # exists
    
    @property
    def isdir(self):
        return self.impl.isdir
    # isdir

    @property
    def isfile(self):
        return self.impl.isfile
    # isfilr

    @property
    def mime_type(self):
        return self.impl.mime_type
    # mime_type
    
    @property
    def size(self):
        return self.impl.size
    # size
    
    def copy_to(self, urifile):
        """
        Copy the binary file represented by this UriFile to the file 
        represented by urifile.
        
        :param UriFile urifile: The target file
        
        :returns: True on success, False on failure
        :rtype: boolean
        """
        buffer = None
        instream = None
        outstream = None
        result = True
        try: 
            instream = self.open_raw_inputstream()
            outstream = urifile.open_raw_outputstream("w")
            while True: 
                buffer = instream.read(4096)
                if len(buffer) > 0:
                    outstream.write(buffer)
                if len(buffer) < 4096: 
                    break
        except BaseException as ex:
            result = False
            self.fnLog(str(ex))
        finally: 
            if instream is not None: 
                instream.close()
            if outstream is not None: 
                outstream.flush()
                outstream.close()
            return result
    # copy_to
    
    def open_raw_inputstream(self):
        """
        Opens a raw stream for reading from file represented by this UriFile
        
        :returns: the binary stream to write to
        :rtype: RawIOBase
        """
        return UriInputStream(self.app, self.uristring, self.fnLog)
    # open_raw_inputstream
        
    def open_raw_outputstream(self, mode):
        """
        Opens a raw stream for writing to the file represented by this UriFile
        
        :param str mode: "w" for overwriting, "a" for appending
        
        :returns: the binary stream to write to
        :rtype: RawIOBase
        """
        return UriOutputStream(self.app, self.uristring, mode, self.fnLog)
    # open_raw_outputstream
# UriFile
