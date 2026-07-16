import asyncio
import mimetypes
import shutil
import tempfile
from pathlib import Path

from rubicon.objc import (
    NSObject,
    ObjCClass,
    ObjCProtocol,
    objc_method,
    send_super,
)


import toga

from .. import urifile
from .. import _security_scoped_urls


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
NSURL = _LazyClass("NSURL")


# ------------------------------------------------------------------------------
# Delegate that receives UIDocumentPickerViewController callbacks.
# Kept alive in _pending_delegates past the future completion (the delegate
# property is weak, so without this the delegate could be deallocated before
# UIKit fully finishes with it, causing EXC_BAD_ACCESS).
# ------------------------------------------------------------------------------

UIDocumentPickerDelegateProtocol = ObjCProtocol("UIDocumentPickerDelegate")

class DocumentPickerDelegate(NSObject, protocols=[UIDocumentPickerDelegateProtocol]):
    @objc_method
    def init(self):
        self = send_super(__class__, self, "init")
        self.future = None
        return self

    @objc_method
    def documentPicker_didPickDocumentsAtURLs_(self, picker, urls):
        if self.future is not None and not self.future.done():
            self.future.set_result(urls)

    @objc_method
    def documentPickerWasCancelled_(self, picker):
        if self.future is not None and not self.future.done():
            self.future.set_result(None)


_pending_delegates = []


# ------------------------------------------------------------------------------
# Security-scoped URL helpers
# ------------------------------------------------------------------------------

def _register_security_scoped_urls(urls):
    """Register security-scoped NSURLs in the global registry so UriFile and
    stream implementations can look them up and call
    startAccessingSecurityScopedResource / stopAccessingSecurityScopedResource
    when performing I/O.

    This function does NOT call startAccessingSecurityScopedResource — that is
    deferred to the actual reader/writer (stream impls) so every start/stop
    pair stays balanced and localised.
    """
    for url in (urls or []):
        if url is not None:
            uristring = str(url.absoluteString())
            if uristring:
                _security_scoped_urls[uristring] = url


# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------

def _build_uttype_array(file_types):
    """Return an NSMutableArray<UTType *> for the given file extension list."""
    print("DEBUG: _build_uttype_array - creating NSMutableArray\n")
    arr = NSMutableArray.alloc().init()
    print("DEBUG: _build_uttype_array - NSMutableArray created\n")
    for ext in file_types or []:
        clean = ext.lstrip(".") if ext.startswith(".") else ext
        print(f"DEBUG: _build_uttype_array - creating UTType for ext={ext!r} clean={clean!r}\n")
        print("DEBUG: creating NSString for enex\n")
        uttype = UTType.typeWithFilenameExtension_(clean)
        print(f"DEBUG: _build_uttype_array - UTType result: {uttype}\n")
        if uttype is not None:
            print("DEBUG: _build_uttype_array - adding UTType to array\n")
            arr.addObject_(uttype)
    print("DEBUG: _build_uttype_array - returning\n")
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
    print("DEBUG: _present_and_await start\n")
    root_vc = _root_view_controller()
    if root_vc is None:
        return None

    print("DEBUG: cleaning pending delegates\n")
    _pending_delegates[:] = [
        (d, p) for d, p in _pending_delegates
        if d.future is None or not d.future.done()
    ]

    print("DEBUG: creating delegate\n")
    delegate = DocumentPickerDelegate.alloc().init()
    print("DEBUG: delegate created\n")
    future = asyncio.get_event_loop().create_future()
    delegate.future = future
    picker.delegate = delegate
    _pending_delegates.append((delegate, picker))

    print("DEBUG: presenting picker\n")
    root_vc.presentViewController_animated_completion_(picker, True, None)

    print("DEBUG: awaiting future\n")
    return await future


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
        print("DEBUG: open_file_dialog start\n")
        uttype_arr = _build_uttype_array(file_types)
        print("DEBUG: uttype count check\n")
        if len(uttype_arr) == 0:
            print("DEBUG: adding fallback public.data\n")
            uttype = UTType.typeWithIdentifier_("public.data")
            print(f"DEBUG: fallback UTType created: {uttype}\n")
            uttype_arr.addObject_(uttype)

        print("DEBUG: creating UIDocumentPickerViewController\n")
        picker = UIDocumentPickerViewController.alloc().initForOpeningContentTypes_(
            uttype_arr
        )
        print("DEBUG: picker created\n")
        print("DEBUG: setting allowsMultipleSelection\n")
        picker.allowsMultipleSelection = multiselect
        print("DEBUG: allowsMultipleSelection set\n")

        if initial_uri:
            path = urifile.uristring_to_ospath(initial_uri)
            if path and Path(path).is_dir():
                picker.directoryURL = NSURL.fileURLWithPath_(path)

        print("DEBUG: calling _present_and_await\n")
        self._picker_uttype_arr = uttype_arr
        try:
            result = await _present_and_await(picker)
        finally:
            self._picker_uttype_arr = None

        if result is None:
            return []

        urls_list = list(result)
        _register_security_scoped_urls(urls_list)

        return [
            str(url.absoluteString())
            for url in urls_list
            if url.absoluteString()
        ]

    async def save_file_dialog(self, title, suggested_filename, file_types):
        tmpdir = Path(tempfile.mkdtemp())
        try:
            tmpfile = tmpdir / (suggested_filename or "untitled")
            Path(tmpfile).touch()
            tmpurl = NSURL.fileURLWithPath_(str(tmpfile))

            export_urls = NSMutableArray.alloc().init()
            export_urls.addObject_(tmpurl)

            picker = UIDocumentPickerViewController.alloc().initForExportingURLs_asCopy_(
                export_urls, False
            )

            result = await _present_and_await(picker)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

        if result is None:
            return None

        urls_list = list(result)
        if len(urls_list) == 0:
            return None

        _register_security_scoped_urls(urls_list)

        url_str = urls_list[0].absoluteString()
        return str(url_str) if url_str else None

    async def select_folder_dialog(self, title, initial_uri=None):
        uttype_arr = NSMutableArray.alloc().init()
        uttype_arr.addObject_(UTType.typeWithIdentifier_("public.folder"))

        picker = UIDocumentPickerViewController.alloc().initForOpeningContentTypes_(
            uttype_arr
        )

        if initial_uri:
            path = urifile.uristring_to_ospath(initial_uri)
            if path and Path(path).is_dir():
                picker.directoryURL = NSURL.fileURLWithPath_(path)

        self._picker_uttype_arr = uttype_arr
        try:
            result = await _present_and_await(picker)
        finally:
            self._picker_uttype_arr = None

        if result is None:
            return None

        urls_list = list(result)
        if len(urls_list) == 0:
            return None

        _register_security_scoped_urls(urls_list)

        url_str = urls_list[0].absoluteString()
        return str(url_str) if url_str else None
