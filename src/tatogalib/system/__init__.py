import json
import sys
import toga


def get_platform():
    """
    Returns the current platform:
    android, iOS, linux, macOS, tvOS, watchOS, wearOS, web, windows

    :returns: The platform string
    :rtype: str
    """
    return toga.platform.current_platform
# get_platform


def get_file_roots(app):
    """
    Returns the file root directories.
    Currently only supported on Android
    
    :param toga.App app: The running toga App
    :returns: The file roots
    :rtype: list[str]
    """
    roots = []
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


def get_startup_arguments(app):
    """
    Returns the arguments passed to the app on startup.
    On Windows, this returns sys.argv, on Android, it returns
    the parsed URL of the main activity. Pass the data as a data URI,
    for example: data:application/json,["arg 1","arg 2"]
    
    :param toga.App app: The running toga App
    :returns: The startup arguments
    :rtype: list[str]
    """
    try:
        argv = []
        if get_platform() == "android":
            argv.append(app.formal_name)
            mainActivity = app._impl.native
            data = mainActivity.getIntent().getDataString()
            if data and data.startswith("data:"):
                lst = data.split(",", 1)
                if len(lst) == 2:
                    j = json.loads(lst[1])
                    if isinstance(j, list):
                        argv = argv + j
        else:
            argv = sys.argv
    except BaseException as ex:
           print(str(ex))
    return argv
# get_startup_arguments