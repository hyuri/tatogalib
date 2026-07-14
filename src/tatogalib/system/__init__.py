import json
import platform
import sys
from urllib.parse import urlparse


def get_platform():
    """
    Returns the current platform via `platform.system()`:
    Android, iOS, iPadOS, Linux, Darwin, Windows, Java

    :returns: The platform string
    :rtype: str
    """
    return platform.system()


# get_platform


def get_file_roots():
    """
    Returns the file root directories.
    Currently only supported on Android and iOS

    :returns: The file roots
    :rtype: list[str]
    """
    roots = []
    import toga
    app = toga.App.app
    try:
        if get_platform() == "Android":
            dirs = app._impl.native.getExternalFilesDirs(None)
            for dir in dirs:
                path = dir.getAbsolutePath()
                idx = path.find("/Android/data/")
                if idx != -1:
                    roots.append(path[0:idx])
        elif get_platform() == "iOS":
            from rubicon.objc import ObjCClass
            NSFileManager = ObjCClass('NSFileManager')
            fm = NSFileManager.defaultManager
            urls = fm.URLsForDirectory_inDomains(9, 1)
            if urls.count > 0:
                roots.append(str(urls[0].path))
        else:
            pass
    except BaseException as ex:
        print(str(ex))
    return roots


# get_file_roots

