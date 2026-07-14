from rubicon.objc import ObjCClass, objc_method, objc_property
from toga.widgets.webview import JavaScriptResult

try:
    from toga_iOS.widgets.base import Widget
except ImportError:
    class Widget:
        def __init__(self, interface):
            self.interface = interface
            self._container = None
            self.native = None
            self.create()

        def set_app(self, app):
            pass

        def set_window(self, window):
            pass

        def set_bounds(self, x, y, width, height):
            if hasattr(self, 'constraints') and self.constraints:
                self.constraints.update(x, y, width, height)

        def add_constraints(self):
            pass

        def rehint(self):
            pass


WKWebView = ObjCClass('WKWebView')
WKWebViewConfiguration = ObjCClass('WKWebViewConfiguration')
NSURL = ObjCClass('NSURL')


class TogaWebView(WKWebView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def webView_didFinishNavigation_(self, webView, navigation):
        if self.interface:
            self.interface.on_webview_load()
        if self.impl and self.impl._loaded_future:
            self.impl._loaded_future.set_result(None)
            self.impl._loaded_future = None


class TaWebViewImpl(Widget):
    SUPPORTS_ON_WEBVIEW_LOAD = True

    def create(self):
        config = WKWebViewConfiguration.alloc().init()
        self.native = TogaWebView.alloc().initWithFrame_configuration_(
            ((0, 0), (0, 0)), config
        )
        self.native.interface = self.interface
        self.native.impl = self
        self.native.navigationDelegate = self.native
        self._loaded_future = None

    def get_url(self):
        url = str(self.native.URL)
        if not url or url == 'about:blank' or url.startswith('data:'):
            return None
        return url

    def set_url(self, value, future=None):
        if value is None:
            value = 'about:blank'
        url = NSURL.URLWithString(value)
        self._loaded_future = future
        self.native.loadRequest_(url)

    def set_content(self, root_url, content):
        base = NSURL.URLWithString(root_url) if root_url else None
        self.native.loadHTMLString_baseURL(content, base)

    def get_user_agent(self):
        return str(self.native.valueForKey_("userAgent")) or ''

    def set_user_agent(self, value):
        self.native.setValue_forKey_(value, "customUserAgent")

    def evaluate_javascript(self, javascript, on_result=None):
        result = JavaScriptResult(on_result)

        def completion_handler(res, error):
            if error:
                result.set_exception(RuntimeError(str(error)))
            else:
                result.set_result(res)

        self.native.evaluateJavaScript_completionHandler(javascript, completion_handler)
        return result

    def set_on_navigation_starting(self, handler):
        pass

    def set_on_resource_requested(self, handler):
        pass

    def cancel_navigation(self, navigation_event):
        navigation_event.cancel = True
