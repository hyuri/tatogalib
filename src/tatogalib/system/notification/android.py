from android import R
from android.app import NotificationManager, NotificationChannel
from android.os import Build
from androidx.core.app import NotificationManagerCompat, NotificationCompat
from datetime import datetime
import toga


class NotificationImpl:
    def __init__(self, interface):
        self.interface = interface
        self.context = toga.App.app._impl.native
        # The channel_id should be unique
        self.CHANNEL_ID = "channel_"+toga.App.app.app_name
        self.notificationManager = None
        channel = self._createNotificationChannel()
        if channel is None:
            self.builder = NotificationCompat.Builder(self.context)
        else:
            self.builder = NotificationCompat.Builder(self.context, self.CHANNEL_ID)
        # self.notificationManager = NotificationManagerCompat.from(self.context)
        fnFrom = getattr(NotificationManagerCompat, "from")
        self.notificationManager = fnFrom(self.context)
    # __init__

    def areNotificationsEnabled(self):
        return self.notificationManager.areNotificationsEnabled()
    # areNotificationsEnabled

    def _createNotificationChannel(self):
        """
        Create the NotificationChannel, but only on API 26+ because
        the NotificationChannel class is not in the Support Library.
        """
        channel = None
        # The channel name and description should be unique
        name = toga.App.app.app_name + " notification channel"
        description = "Channel for displaying notifications from " + toga.App.app.app_name
        if Build.VERSION.SDK_INT >= Build.VERSION_CODES.O:
            importance = NotificationManager.IMPORTANCE_DEFAULT
            channel = NotificationChannel(self.CHANNEL_ID, name, importance)
            channel.setDescription(description)
            # Register the channel with the system. You can't change the importance
            # or other notification behaviors after this.
            notificationManager = self.context.getSystemService(NotificationManager)
            notificationManager.createNotificationChannel(channel)
        return channel
        # _createNotificationChannel

    def notify(self, title, message, icon):
        if icon is None:
            icon = R.drawable.ic_dialog_info
        self.builder.setSmallIcon(icon)
        self.builder.setContentTitle(title)
        self.builder.setContentText(message)
        self.builder.setStyle(NotificationCompat.BigTextStyle().bigText(message))
        self.builder.setPriority(NotificationCompat.PRIORITY_DEFAULT)
        notification = self.builder.build()
        # notificationId is a unique int for each notification that you must define
        notificationId = NotificationImpl._todays_millis()
        return self.notificationManager.notify(notificationId, notification)

    # notify
    
    @staticmethod
    def _todays_millis():
        """
        Milliseconds since midnight. This creates a unique value for 1 day
        and is most probably also unique when called over several days.
        """
        now = datetime.now()
        midnight = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        msec = int(now.timestamp()*1000 - midnight.timestamp()*1000)
        return msec

    # _todays_millis

# NotificationImpl


version = "0.5.0"
version_date = "2023-06-14 - 2023-06-14"
