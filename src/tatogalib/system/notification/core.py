import toga


class Notification:
    def __init__(self, fnLog=None):
        """
        Creates a system notification.

        :param callable fnLog: The callable which is called from the log method
            It expects a string parameter
        """
        self._fnlog = fnLog  # for logging to user code
        self._impl = None
        if toga.platform.current_platform == "android":
            from .android import NotificationImpl
        else:
            raise NotImplementedError(f"Notification is not implemented for {toga.platform.current_platform}")
        self._impl = NotificationImpl(self)

    # __init__
    
    def notify(self, title, message):
        """
        Displays the notification and returns its id.
        
        :param str title: The title of the notification
        :param str message: The message of the notification

        :returns: the shown notification
        :rtype: int   
        """
        self._impl.notify(title, message)
    # notify

    def log(self, message):
        """
        Logs a message to the user code if fnLog was passed to the constructor

        :param str message: The message to be logged
        """
        if self._fnlog is not None:
            self._fnlog(message)

    # log

# Notification


version = "0.2.0"
version_date = "2023-06-14 - 2023-06-14"
