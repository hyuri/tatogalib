import toga

if toga.platform.current_platform == "android":
    from .android import UriInputStream
if toga.platform.current_platform == "windows":
    from .windows import UriInputStream
