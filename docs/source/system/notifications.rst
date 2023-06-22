notifications package
=====================

This package allows to post system notifications on Android and Windows.

Example:

.. code-block:: Python

   from tatogalib.system.notifications import AppIcon

   # importing tatogalib.system.notifications has created the member
   # self.app.notifications which is the NotificationManager

   print(f"Notifications enabled: {self.app.notifications.are_notifications_enabled()}")
   id = self.app.notifications.post_notification("My title", text, AppIcon.INFO)


.. toctree::
   :maxdepth: 2

.. automodule:: tatogalib.system.notifications
   :members:

AppIcon class
-------------
.. autoclass:: tatogalib.system.notifications.AppIcon
   :members:

NotificationManager class
-------------------------
.. autoclass:: tatogalib.system.notifications.NotificationManager
   :members:
