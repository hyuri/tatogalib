import os
from pathlib import Path
from urllib.parse import urlparse, unquote
from urllib.request import url2pathname
from .core import UriFile


def ospath_to_uristring(ospath):
    """
    Converts an os.path to an URI-string (file://)
    Returns None if conversion is not possible

    :param str ospath: The path string

    :returns: The URI-string
    :rtype: str or None
    """
    result = None
    if type(ospath) is not str:
        return result
    result = Path(os.path.abspath(ospath)).as_uri()
    return result


# ospath_to_uristring


def uristring_to_ospath(uristring):
    """
    Converts a URI-string to an os.path. This will generally only be possible
    for file:// URI-strings.
    Returns None if conversion is not possible

    :param str uristring: The URI-string

    :returns: The path string
    :rtype: str or None
    """
    result = None
    if type(uristring) is not str or not uristring.startswith("file://"):
        return result
    parsed = urlparse(uristring)
    host = "{0}{0}{mnt}{0}".format(os.path.sep, mnt=parsed.netloc)
    return os.path.normpath(os.path.join(host, url2pathname(unquote(parsed.path))))


# uristring_to_ospath
