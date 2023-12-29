import json
import sys
import toga
from urllib.parse import urlparse


def get_platform():
    """
    Returns the current platform:
    android, iOS, linux, macOS, tvOS, watchOS, wearOS, web, windows

    :returns: The platform string
    :rtype: str
    """
    return toga.platform.current_platform


# get_platform


def get_file_roots():
    """
    Returns the file root directories.
    Currently only supported on Android

    :returns: The file roots
    :rtype: list[str]
    """
    roots = []
    app = toga.App.app
    try:
        if get_platform() == "android":
            dirs = app._impl.native.getExternalFilesDirs(None)
            for dir in dirs:
                path = dir.getAbsolutePath()
                idx = path.find("/Android/data/")
                if idx != -1:
                    roots.append(path[0:idx])
        else:
            # todo: implement for other platforms
            pass
    except BaseException as ex:
        print(str(ex))
    return roots


# get_file_roots

