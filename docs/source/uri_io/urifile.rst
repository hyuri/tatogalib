urifile package
===============

This package allows to work with files and directories in a cross-platform way.
It has been tested on Android and Windows, but should also work on Linux and macOS.

Example for displaying the content of a folder:

.. code-block:: Python

   from tatogalib.uri_io.urifile import UriFile
   
   uristring = "content://com.android.externalstorage.documents/document/primary%3ADaten"
   folder = UriFile(uristring)
   children = folder.listdir()
   if children is None:
       print("Uri is not a folder")
   for urifile in children:
       print(f"name: {urifile.name}")
       print(f"uristring: {urifile.uristring}")
       print(f"isdir: {urifile.isdir()}")
       print(f"size: {urifile.size}")

Example for reading a file:

.. code-block:: Python

   from tatogalib.uri_io.urifile import UriFile
   
   uristring = "content://com.android.externalstorage.documents/document/primary%3ADaten/test.txt"
   myfile = UriFile(uristring)
   f = myfile.open("rt", "utf-8-sig")
   bytesobj = f.read()
   f.close()
   print(str(bytesobj)


.. toctree::
   :maxdepth: 2
   
.. automodule:: tatogalib.uri_io.urifile
   :members:

UriFile class
-------------
.. autoclass:: tatogalib.uri_io.urifile.core.UriFile
   :members:
