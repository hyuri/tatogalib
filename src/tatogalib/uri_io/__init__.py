# Registry for security-scoped NSURLs returned by the iOS document picker.
# Key: URI string (e.g. "file:///path/to/file")
# Value: the rubicon-objc NSURL object
# Only populated on iOS when a file is selected via UIDocumentPickerViewController.
_security_scoped_urls: dict[str, object] = {}
