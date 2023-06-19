from datetime import datetime
import toga
from toga_winforms.libs.winforms import WinForms
from System.Drawing import SystemIcons


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

    def post_notification(self, notification):
        if notification.icon is None:
            notification.icon = SystemIcons.Information
        notifyIcon = WinForms.NotifyIcon()
        notifyIcon.Icon = notification.icon
        notifyIcon.BalloonTipTitle = notification.title
        notifyIcon.BalloonTipText = notification.message
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


version = "0.8.0"
version_date = "2023-06-14 - 2023-06-18"
