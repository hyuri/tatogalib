from ... import system

if system.get_platform() == "Android":
    from .core import TaSelection
else:
    from toga import Selection as TaSelection
