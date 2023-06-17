import toga


class Notification:
    def __init__(self, title, message, icon=None):
        """
        Creates a notification.

        :param str title: The title of the notification
        :param str message: The message of the notification
        :param int icon: On Android, this must be a resource ID.
            If None, R.drawable.ic_dialog_info is used.
        """
        self.title = title
        self.message = message
        self.icon = icon
        self.id = None
    # __init__
    
    @property
    def title(self):
        return self._title
        
    @title.setter
    def title(self, title):
        self._title = title

    @property
    def message(self):
        return self._message
        
    @message.setter
    def message(self, message):
        self._message = message

    @property
    def icon(self):
        return self._icon
        
    @icon.setter
    def icon(self, icon):
        self._icon = icon

    @property
    def id(self):
        """
        The id of the notification. It is set, when the
        notification is shown.
        """
        return self._id
        
    @id.setter
    def id(self, id):
        self._id = id
 
# Notification

class NotificationManager:
    def __init__(self, fnLog=None):
        """
        Creates a manager for handling system notification.

        On Android, the app needs the permission android.permission.POST_NOTIFICATIONS
        and the notifications must be enabled for the app in the Android settings.

        :param callable fnLog: The callable which is called from the log method.
            It expects a string parameter
        """
        self._fnlog = fnLog  # for logging to user code
        self._impl = None
        if toga.platform.current_platform == "android":
            from .android import NotificationManagerImpl
        else:
            raise NotImplementedError(
                f"Notification is not implemented for {toga.platform.current_platform}"
            )
        self._impl = NotificationManagerImpl(self)

    # __init__

    def are_notifications_enabled(self):
        """
        Checks if notifications are enabled

        :returns: True when enabled, False otherwise
        :rtype: boolean
        """
        return self._impl.are_notifications_enabled()

    # are_notifications_enabled

    def show_notification(self, notification):
        """
        Displays the notification and returns its id.
        The id is also set in the notification object.

        :param Notification notification: The notification to show

        :returns: the id of the displayed notification
        :rtype: int
        """
        notification.id = self._impl.show_notification(notification)
        return notification.id

    # show_notification

    def log(self, message):
        """
        Logs a message to the user code if fnLog was passed to the constructor

        :param str message: The message to be logged
        """
        if self._fnlog is not None:
            self._fnlog(message)

    # log


# NotificationManager


version = "0.6.0"
version_date = "2023-06-14 - 2023-06-17"
