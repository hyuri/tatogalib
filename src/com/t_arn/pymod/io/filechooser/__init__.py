import toga

if toga.platform.current_platform == "android":
    from .android import FileChooser
if toga.platform.current_platform == "windows":
    from .windows import FileChooser
