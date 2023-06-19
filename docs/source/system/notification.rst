notification package
====================

This package allows to post system notifications.

Example:

.. code-block:: Python

   from system.notification import Notification, NotificationManager

   mgr = NotificationManager()
   print(f"Notifications enabled: {mgr.are_notifications_enabled()}")
   notification = Notification("My title", text, 17301543)  # R.drawable.ic_dialog_alert
   id = mgr.post_notification(notification)


.. toctree::
   :maxdepth: 2

.. automodule:: tatogalib.system.notification
   :members:

Notification class
------------------
.. autoclass:: tatogalib.system.notification.core.Notification
   :members:

NotificationManager class
-------------------------
.. autoclass:: tatogalib.system.notification.core.NotificationManager
   :members:
