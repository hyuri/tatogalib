import toga

from ... import system


class AppIcon:
    """ """

    APP = 0
    """
    """
    INFO = 1
    """
    """
    QUESTION = 2
    """
    """
    WARNING = 3
    """
    """
    ERROR = 4
    """
    """


# AppIcon


class NotificationManager:
    def __init__(self, fnLog=None):
        """
        Creates a manager for handling system notifications.

        On Android, the app needs the permission android.permission.POST_NOTIFICATIONS
        and the notifications must be enabled for the app in the Android settings.

        :param callable fnLog: The callable which is called from the log method.
            It expects a string parameter
        """
        self._fnlog = fnLog  # for logging to user code
        self._impl = None
        plat = system.get_platform()
        if plat == "Android":
            from .android import NotificationManagerImpl
        elif plat == "Windows":
            from .windows import NotificationManagerImpl
        else:
            raise NotImplementedError(
                f"Notification is not implemented for {plat}"
            )
        self._impl = NotificationManagerImpl(self)
        toga.App.app.notifications = NotificationManager()

    # __init__

    def are_notifications_enabled(self):
        """
        Checks if notifications are enabled

        :returns: True when enabled, False otherwise
        :rtype: boolean
        """
        return self._impl.are_notifications_enabled()

    # are_notifications_enabled

    def cancel_notification(self, id):
        """
        Cancel a previously shown notification

        :param int id: The id of the notification
        """
        self._impl.cancel_notification(id)

    # cancel_notification

    def cancel_all_notifications(self):
        """
        Cancel all previously shown notification
        """
        self._impl.cancel_all_notifications()

    # cancel_all_notifications

    def post_notification(self, title, message, icon=None):
        """
        Post and displays the notification and returns its id.
        The optional icon can be one of following 3 cases:

        | 1. None will default to the app's icon.
        | 2. AppIcon is a system provided icon.
        | 3. String with the path to an app-specific icon file,
        | e.g. self.app.paths.app / "resources" / "notification_icon.png"

        :param str title: The title of the notification
        :param str message: The message of the notification
        :param None or AppIcon or str icon: The icon of the notification

        :returns: the id of the posted notification
        :rtype: int
        """
        if icon is None:
            icon = AppIcon.APP
        id = self._impl.post_notification(title, message, icon)
        return id

    # post_notification

    def log(self, message):
        """
        Logs a message to the user code if fnLog was passed to the constructor

        :param str message: The message to be logged
        """
        if self._fnlog is not None:
            self._fnlog(message)

    # log

    def set_log(self, fnLog=None):
        """
        Sets a log method for debugging.

        :param callable fnLog: The callable which is called from the log method.
            It expects a string parameter
        """
        self._fnlog = fnLog

    # set_log


# NotificationManager


version = "0.9.1"
version_date = "2023-06-14 - 2023-06-23"
