notification package
====================

This package allows to post system notifications on Android and Windows.

Example:

.. code-block:: Python

   from tatogalib.system.notifications import Notification, NotificationManager, AppIcon
   from Android import R

   mgr = NotificationManager()
   print(f"Notifications enabled: {mgr.are_notifications_enabled()}")
   notification = Notification("My title", text, AppIcon.INFO)
   id = mgr.post_notification(notification)


.. toctree::
   :maxdepth: 2

.. automodule:: tatogalib.system.notifications
   :members:

AppIcon class
-------------
.. autoclass:: tatogalib.system.notifications.core.AppIcon
   :members:

Notification class
------------------
.. autoclass:: tatogalib.system.notifications.core.Notification
   :members:

NotificationManager class
-------------------------
.. autoclass:: tatogalib.system.notifications.core.NotificationManager
   :members:
