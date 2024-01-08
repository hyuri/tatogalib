clipboard package
=================

This package allows to access the system clipboard on Android and Windows.
It currently only supports text. If you want to work with binary content, you
might want to use base64 encoding.

Example:

.. code-block:: Python

   from tatogalib.system.clipboard import Clipboard

   cb = Clipboard.get_clipboard()
   cb.set_text("Text to be copied into the clipboard")
   clip_text = cb.get_text()


.. toctree::
   :maxdepth: 2

.. automodule:: tatogalib.system.clipboard
   :members:

Clipboard class
---------------
.. autoclass:: tatogalib.system.clipboard.Clipboard
   :members:
