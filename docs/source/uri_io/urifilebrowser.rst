urifilebrowser package
=======================

This package allows to select files and directories in a cross-platform way.
It currently supports Android and Windows.

Example:

.. code-block:: Python

   from uri_io.urifilebrowser import UriFileBrowser
   from uri_io.urifile import UriFile
   
   fb = UriFileBrowser()
   initial = "content://com.android.externalstorage.documents/document/primary%3ADaten"
   urilist = await fb.open_file_dialog(
       "Choose a file",
       file_types=["xlsx","pdf","rar"], 
       multiselect=True, 
       initial_uri=initial
   ) 
   if len(urilist) > 0:
       urifile = UriFile(urilist[0])

.. toctree::
   :maxdepth: 2
   
.. automodule:: tatogalib.uri_io.urifilebrowser
   :members:

UriFileBrowser class
--------------------
.. autoclass:: tatogalib.uri_io.urifilebrowser.core.UriFileBrowser
   :members:
