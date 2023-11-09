from datetime import datetime
import toga
from toga_winforms.libs.winforms import WinForms
from System.Drawing import SystemIcons
from .core import AppIcon


class NotificationManagerImpl:
    notification_list = []

    def __init__(self, interface):
        self.interface = interface

    # __init__

    def are_notifications_enabled(self):
        return True

    # are_notifications_enabled

    def cancel_notification(self, id):
        for item in self.notification_list:
            (notificationId, obj) = item
            if notificationId == id:
                obj.Dispose()
                self.notification_list.remove(item)

    # cancel_notification

    def cancel_all_notifications(self):
        for item in self.notification_list:
            (notificationId, obj) = item
            obj.Dispose()
        self.notification_list.clear()

    # cancel_all_notifications

    def post_notification(self, title, message, icon):
        if type(icon) is int:
            if icon == AppIcon.APP:
                native_icon = toga.App.app.icon._impl.native
            elif icon == AppIcon.INFO:
                native_icon = SystemIcons.Information
            elif icon == AppIcon.QUESTION:
                native_icon = SystemIcons.Question
            elif icon == AppIcon.WARNING:
                native_icon = SystemIcons.Warning
            elif icon == AppIcon.ERROR:
                native_icon = SystemIcons.Error
            else:
                raise AttributeError(
                    "NotficationManager.post_notification(): unsupported system icon"
                )
        elif type(icon) is str:
            toga_icon = toga.Icon(icon)
            native_icon = toga_icon._impl.native
        else:
            raise AttributeError(
                "NotficationManager.post_notification(): unsupported icon type"
            )
        notifyIcon = WinForms.NotifyIcon()
        notifyIcon.Icon = native_icon
        notifyIcon.BalloonTipTitle = title
        notifyIcon.BalloonTipText = message
        notifyIcon.Visible = True
        notifyIcon.ShowBalloonTip(30000)
        notificationId = NotificationManagerImpl._todays_millis()
        self.notification_list.append((notificationId, notifyIcon))
        return notificationId

    # post_notification

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


version = "0.9.1"
version_date = "2023-06-14 - 2023-06-23"
