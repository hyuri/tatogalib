from android import R
from android.app import Notification, NotificationManager, NotificationChannel
from android.graphics.drawable import Icon as A_Icon
from android.os import Build
from datetime import datetime
import toga
from .core import AppIcon


class NotificationManagerImpl:
    def __init__(self, interface):
        self.interface = interface
        self.context = toga.App.app._impl.native
        self.notificationManager = self.context.getSystemService(NotificationManager)
        # The channel_id should be unique
        self.CHANNEL_ID = "channel_" + toga.App.app.app_name
        channel = self._createNotificationChannel()
        if channel is None:
            self.builder = Notification.Builder(self.context)
        else:
            self.builder = Notification.Builder(self.context, self.CHANNEL_ID)

    # __init__

    def are_notifications_enabled(self):
        return self.notificationManager.areNotificationsEnabled()

    # are_notifications_enabled

    def cancel_notification(self, id):
        self.notificationManager.cancel(id)

    # cancel_notification

    def cancel_all_notifications(self):
        self.notificationManager.cancelAll()

    # cancel_all_notifications

    def _createNotificationChannel(self):
        """
        Create the NotificationChannel, but only on API 26+ because
        the NotificationChannel class is not in the Support Library.
        """
        channel = None
        # The channel name and description should be unique
        name = toga.App.app.app_name + " notification channel"
        description = (
            "Channel for displaying notifications from " + toga.App.app.app_name
        )
        if Build.VERSION.SDK_INT >= Build.VERSION_CODES.O:
            importance = NotificationManager.IMPORTANCE_DEFAULT
            channel = NotificationChannel(self.CHANNEL_ID, name, importance)
            channel.setDescription(description)
            # Register the channel with the system. You can't change the importance
            # or other notification behaviors after this.
            self.notificationManager.createNotificationChannel(channel)
        return channel

        # _createNotificationChannel

    def post_notification(self, title, message, icon):
        if type(icon) is int:
            if icon == AppIcon.APP:
                native_icon = self._get_app_icon()
            elif icon == AppIcon.INFO:
                native_icon = R.drawable.ic_dialog_info
            elif icon == AppIcon.QUESTION:
                native_icon = R.drawable.ic_menu_help
            elif icon == AppIcon.WARNING:
                native_icon = R.drawable.ic_dialog_alert
            elif icon == AppIcon.ERROR:
                native_icon = R.drawable.ic_delete
            else:
                raise AttributeError(
                    "NotficationManager.post_notification(): unsupported system icon"
                )
        elif type(icon) is str:
            native_icon = self._get_custom_icon(icon)
        else:
            raise AttributeError(
                "NotficationManager.post_notification(): unsupported icon type"
            )
        self.builder.setSmallIcon(native_icon)
        self.builder.setContentTitle(title)
        self.builder.setContentText(message)
        self.builder.setStyle(Notification.BigTextStyle().bigText(message))
        self.builder.setPriority(Notification.PRIORITY_DEFAULT)
        native_notification = self.builder.build()
        # notificationId is a unique int for each notification that you must define
        notificationId = NotificationManagerImpl._todays_millis()
        self.notificationManager.notify(notificationId, native_notification)
        return notificationId

    # post_notification

    def _get_app_icon(self):
        res = self.context.getResources()
        pkg = self.context.getApplicationInfo().packageName
        return res.getIdentifier("ic_launcher", "mipmap", pkg)

    # _get_app_icon

    def _get_custom_icon(self, path):
        stream = open(path, "rb", buffering=0)
        bytes = stream.read()
        stream.close()
        native_icon = A_Icon.createWithData(bytes, 0, len(bytes))
        return native_icon

    # _get_custom_icon

    @staticmethod
    def _todays_millis():
        """
        Milliseconds since midnight. This creates a unique value for 1 day
        and is most probably also unique when called over several days.
        """
        now = datetime.now()
        midnight = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        msec = int(now.timestamp() * 1000 - midnight.timestamp() * 1000)
        return msec

    # _todays_millis


# NotificationManagerImpl


version = "0.9.0"
version_date = "2023-06-14 - 2023-06-23"
