import toga
from ..uriinputstream import UriInputStream
from ..urioutputstream import UriOutputStream

class UriFile:
    
    def __init__(self, uristring, is_file=True, fnLog=None):
        """
        Creates a UriFile which represents a file or a folder
        
        :param str uristring: A URI-string representing this UriFile object
        :param boolean is_file: True when uristring represents a file, False for a folder
        :param callable fnLog: The callable which is called from the log method
            It expects a string parameter
        """
        self.uristring = uristring
        self._fnlog = fnLog  # for logging to user code
        if toga.platform.current_platform == "android":
            from .android import UriFileImpl
        if toga.platform.current_platform == "windows":
            from .desktop import UriFileImpl
        self._impl = UriFileImpl(self, is_file)
    # __init__

    @property
    def display_name(self):
        """
        The name (str) of the file or folder
        """
        return self._impl.get_display_name()
    # display_name
    
    @property
    def lastmodified(self): 
        """
        The last modification time (int) of the file or folder.
        It is the amount of seconds since 1970-01-01T00:00:00
        """
        return self._impl.get_lastmodified()
        
    def set_lastmodified(self, unixtime):
        """
        Sets the last modification time (int) of the file or folder.
        
        :param int unixtime: amount of seconds since 1970-01-01T00:00:00
        
        :returns: True on success, False on failure
        :rtype: boolean
        """
        return self._impl.set_lastmodified(unixtime)
    # lastmodified    

    @property
    def mime_type(self):
        """
        The MIME type (e.g. "application/pdf") of the file.
        Returns None if type cannot be evaluated
        """
        return self._impl.get_mime_type()
    # mime_type
    
    @property
    def size(self):
        """
        The size (int) of the file
        """
        return self._impl.get_size()
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
            instream.close()
            instream = None
            outstream.flush()
            outstream.close()
            outstream = None
        except BaseException as ex:
            if instream is not None: 
                instream.close()
            if outstream is not None: 
                outstream.flush()
                outstream.close()
            urifile.delete()
            result = False
            self.log(str(ex))
        finally: 
            return result
    # copy_to
    
    def delete(self): 
        """
        Deletes the file
        
        :returns: True on success, False on failure
        :rtype: boolean
        """
        return self._impl.delete()
    # delete
    
    def exists(self):
        """
        Checks if the file or folder exists
        
        :returns: True when exists, False otherwise
        :rtype: boolean
        """
        return self._impl.exists()
    # exists
    
    def isdir(self):
        """
        Checks if the UriFile represents an existing folder
        
        :returns: True or False
        :rtype: boolean
        """
        return self._impl.isdir()
    # isdir

    def isfile(self):
        """
        Checks if the UriFile represents an existing file
                
        :returns: True or False
        :rtype: boolean
        """
        return self._impl.isfile()
    # isfile
    
    def log(self, message):
        """
        Logs a message to the user code if fnLog was passed to the constructor
        
        :param str message: The message to be logged
        """
        if self._fnlog is not None:
            self._fnlog(message)
    # log

    def open_raw_inputstream(self):
        """
        Opens a rawIO stream for reading from the file represented by this UriFile
        
        :returns: the binary stream to read from
        :rtype: RawIOBase
        """
        return UriInputStream(self.uristring, self._fnlog)
    # open_raw_inputstream
        
    def open_raw_outputstream(self, mode):
        """
        Opens a rawIO stream for writing to the file represented by this UriFile
        
        :param str mode: "w" for overwriting, "a" for appending
        
        :returns: the binary stream to write to
        :rtype: RawIOBase
        """
        return UriOutputStream(self.uristring, mode, self._fnlog)
    # open_raw_outputstream

    def open_text_inputstream(self, encoding):
        """
        Opens a text stream for reading from the file represented by this UriFile
        
        :param str encoding: The encoding to use for converting the bytes to text
        :returns: the text stream to read from
        :rtype: TextIOWrapper
        """
        return UriTextInputStream(self.uristring, encoding, self._fnlog)
    # open_raw_inputstream
    
# UriFile


version = "0.5.0"
version_date = "2023-05-23 - 2023-05-23"
