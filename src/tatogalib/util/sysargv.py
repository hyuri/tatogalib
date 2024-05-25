import sys


class SysArgv:
    """
    Class for parsing commandline arguments.
    All arguments must be an option string with
    or without a value, e.g.
    
    myapp --cli --infilename myinfile --outfilename "my out file"
    
    args = SysArgs()
    args.get("cli")          # returns True
    args.get("infilename")   # returns "myinfile"
    args.get("outfilename")  # returns "my out file"
    args.get("whatever")     # returns None
    """
    _args = {}
    
    def __init__(self):
        lastoption = None
        for arg in sys.argv:
            if arg.startswith("--"):
                lastoption = arg[2:]
                self._args[lastoption] = True
            else:
                if lastoption is not None:
                    self._args[lastoption] = arg
                    lastoption = None
                else:
                    pass  # ignore this value
    # __init__
    
    def get(self, option_name):
        """
        Get a commandline argument identified by its option name.
        Returns None if the option name does not exist.
        
        :param str option_name: The name of the option string
        :returns: The value of the option string or None
        """
        try:
            return self._args[option_name]
        except KeyError:
            return None
    # get
    
    def get_all(self):
        """
        Get all commandline arguments
        
        :returns: The dictionary with the option names and their values
        """
        return self._args
    # get_all

    def length(self):
        """
        Gets the number of parsed arguments
        
        :returns: number of arguments
        """
        return len(self._args)
    # length

# SysArgv
