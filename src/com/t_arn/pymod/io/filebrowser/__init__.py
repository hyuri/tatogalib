import toga

if toga.platform.current_platform == "android":
    from .android import FileBrowser
if toga.platform.current_platform in ("windows","macOS","linux"):
    from .desktop import FileBrowser
