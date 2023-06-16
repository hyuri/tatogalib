import toga


class Notification:
    def __init__(self, fnLog=None):
        """
        Creates a system notification. 

        On Android, the app needs the permission android.permission.POST_NOTIFICATIONS
        and the notifications must be enabled for the app in the Android settings.

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

    def areNotificationsEnabled(self):
        """
        Checks if notifications are enabled
        
        :returns: True when enabled, False otherwise
        :rtype: boolean
        """
        return self._impl.areNotificationsEnabled()
    # areNotificationsEnabled

    def notify(self, title, message, icon=None):
        """
        Displays the notification and returns its id.
        
        :param str title: The title of the notification
        :param str message: The message of the notification
        :param int icon: On Android, this must be a resource ID
            If None, R.drawable.ic_dialog_info is used

        :returns: the id of the displayed notification
        :rtype: int   
        """
        self._impl.notify(title, message, icon)
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


version = "0.5.0"
version_date = "2023-06-14 - 2023-06-14"
