import toga

if toga.platform.current_platform == "android":
    from .android import FileBrowser
if toga.platform.current_platform == "windows":
    from .windows import FileBrowser
