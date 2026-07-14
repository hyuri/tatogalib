import asyncio
import mimetypes
from pathlib import Path

from rubicon.objc import (
    NSObject,
    objc_method,
    ObjCClass,
    send_super,
)
from rubicon.objc.api import NSString

import toga

from .. import urifile


# ------------------------------------------------------------------------------
# ObjC class references (lazy-loaded on first use so the module can be imported
# on macOS without crashing; on iOS all UIKit classes are guaranteed available).
# ------------------------------------------------------------------------------

class _LazyClass:
    """Wrapper that loads an ObjC class on first attribute access."""

    def __init__(self, name):
        self._name = name
        self._cls = None

    def __getattr__(self, name):
        if self._cls is None:
            self._cls = ObjCClass(self._name)
        return getattr(self._cls, name)

    def __call__(self, *args, **kwargs):
        if self._cls is None:
            self._cls = ObjCClass(self._name)
        return self._cls(*args, **kwargs)


UIDocumentPickerViewController = _LazyClass("UIDocumentPickerViewController")
UTType = _LazyClass("UTType")
NSMutableArray = ObjCClass("NSMutableArray")


# ------------------------------------------------------------------------------
# Delegate that receives UIDocumentPickerViewController callbacks.
# Kept alive by _pending_delegates until the future completes (the delegate
# property is weak, so without this the delegate would be deallocated early).
# ------------------------------------------------------------------------------

class DocumentPickerDelegate(NSObject, protocols=["UIDocumentPickerDelegate"]):
    @objc_method
    def init(self):
        self = send_super(__class__, self, "init")
        self.future = None
        return self

    @objc_method
    def documentPicker_didPickDocumentsAtURLs_(self, picker, urls):
        if self.future is not None and not self.future.done():
            result = [urls.objectAtIndex_(i) for i in range(urls.count())]
            self.future.set_result(result)

    @objc_method
    def documentPickerWasCancelled_(self, picker):
        if self.future is not None and not self.future.done():
            self.future.set_result(None)


_pending_delegates = set()


# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------

def _build_uttype_array(file_types):
    """Return an NSMutableArray<UTType *> for the given file extension list."""
    arr = NSMutableArray.alloc().init()
    for ext in file_types or []:
        clean = ext.lstrip(".") if ext.startswith(".") else ext
        uttype = UTType.typeWithFilenameExtension_(NSString(clean))
        if uttype is not None:
            arr.addObject_(uttype)
    return arr


def _root_view_controller():
    """Return the topmost UINavigationController for presenting dialogs."""
    app = toga.App.app
    try:
        return app.main_window._impl.container.controller
    except AttributeError:
        return None


async def _present_and_await(picker):
    """Present a UIDocumentPickerViewController and await the user's choice."""
    root_vc = _root_view_controller()
    if root_vc is None:
        return None

    delegate = DocumentPickerDelegate.alloc().init()
    future = asyncio.get_event_loop().create_future()
    delegate.future = future
    picker.delegate = delegate
    _pending_delegates.add(delegate)

    root_vc.presentViewController_animated_completion_(picker, True, None)

    try:
        return await future
    finally:
        _pending_delegates.discard(delegate)


# ------------------------------------------------------------------------------
# Implementation
# ------------------------------------------------------------------------------

class UriFileBrowserImpl:
    def __init__(self, interface):
        self.interface = interface
        self.app = toga.App.app

    def uri_infos(self, uristring):
        infos = {}
        if uristring is None:
            return infos
        try:
            path = Path(urifile.uristring_to_ospath(uristring))
            infos["display_name"] = path.name
            infos["size"] = path.stat().st_size
            (mime_type, encoding) = mimetypes.guess_type(uristring, strict=False)
            if mime_type is None:
                self.interface.log(f"Can't guess MIME type for {uristring}")
            infos["type"] = mime_type
        except BaseException as ex:
            self.interface.log(str(ex))
        finally:
            return infos

    async def open_file_dialog(self, title, initial_uri, file_types, multiselect):
        uttype_arr = _build_uttype_array(file_types)
        if uttype_arr.count() == 0:
            uttype_arr.addObject_(UTType.typeWithIdentifier_(NSString("public.data")))

        picker = UIDocumentPickerViewController.alloc().initForOpeningContentTypes_(
            uttype_arr
        )
        picker.allowsMultipleSelection = multiselect

        result = await _present_and_await(picker)
        if result is None:
            return []

        return [
            str(url.absoluteString())
            for url in result
            if url.absoluteString()
        ]

    async def save_file_dialog(self, title, suggested_filename, file_types):
        uttype_arr = _build_uttype_array(file_types)
        if uttype_arr.count() == 0:
            uttype_arr.addObject_(UTType.typeWithIdentifier_(NSString("public.data")))

        picker = UIDocumentPickerViewController.alloc().initForExportingContentTypes_(
            uttype_arr
        )

        result = await _present_and_await(picker)
        if result is None or len(result) == 0:
            return None

        url_str = result[0].absoluteString()
        return str(url_str) if url_str else None

    async def select_folder_dialog(self, title, initial_uri=None):
        uttype_arr = NSMutableArray.alloc().init()
        uttype_arr.addObject_(UTType.typeWithIdentifier_(NSString("public.folder")))

        picker = UIDocumentPickerViewController.alloc().initForOpeningContentTypes_(
            uttype_arr
        )

        result = await _present_and_await(picker)
        if result is None or len(result) == 0:
            return None

        url_str = result[0].absoluteString()
        return str(url_str) if url_str else None
