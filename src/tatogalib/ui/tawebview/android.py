import json

from android.webkit import ValueCallback, WebView as A_WebView, WebViewClient, WebResourceRequest
from java import dynamic_proxy, static_proxy, constructor, jboolean, jclass, Override

from toga.widgets.webview import JavaScriptResult

# from .base import Widget
from toga_android.widgets.base import Widget


class ReceiveString(dynamic_proxy(ValueCallback)):
    def __init__(self, result):
        super().__init__()
        self.result = result

    def onReceiveValue(self, value):
        # If the evaluation fails, a message is written to Logcat, but the value sent to
        # the callback will be "null", with no way to distinguish it from an actual null
        # return value.
        res = json.loads(value)

        self.result.set_result(res)


class TogaNavigationEvent():
    def __init__(self, webresourcerequest):
        self.request = webresourcerequest
        self.cancel = False
    # __init__
# TogaNavigateToEvent
    

class TogaWebClient(static_proxy(WebViewClient)):
    @constructor([jclass])
    def __init__(self, impl):
        super().__init__()
        self.webview_impl = impl
    # __init__

    @Override(jboolean, [jclass, jclass])
    def shouldOverrideUrlLoading(webview, webresourcerequest):
        if self.webview_impl.interface.on_navigation_starting:
            event = TogaNavigationEvent(webresourcerequest)
            self.webview_impl.interface.on_navigation_starting(
                webresourcerequest.getUrl().toString(),
                event
            )
            # if navigation should be aborted, the user code 
            # must call cancel_navigation(event)
            if event.cancel == True:
                event = None
                return True
        return super().shouldOverrideUrlLoading(webview, webresourcerequest)
    # shouldOverrideUrlLoading
# TogaWebClient


# class WebView(Widget):
class TaWebViewImpl(Widget):
    SUPPORTS_ON_WEBVIEW_LOAD = False

    def create(self):
        self.native = A_WebView(self._native_activity)
        # Set a WebViewClient so that new links open in this activity,
        # rather than triggering the phone's web browser.
        # self.native.setWebViewClient(WebViewClient())
        client = TogaWebClient(self)
        self.native.setWebViewClient(client)

        self.settings = self.native.getSettings()
        self.default_user_agent = self.settings.getUserAgentString()
        self.settings.setJavaScriptEnabled(True)
        self.settings.setDomStorageEnabled(True)
        # enable pinch-to-zoom without the deprecated on-screen controls
        self.settings.setBuiltInZoomControls(True)
        self.settings.setDisplayZoomControls(False)

    def get_url(self):
        url = self.native.getUrl()
        if url == "about:blank" or url.startswith("data:"):
            return None
        else:
            return url

    def set_url(self, value, future=None):
        if value is None:
            value = "about:blank"
        self.native.loadUrl(value)

        # Detecting when the load is complete requires subclassing WebViewClient
        # (https://github.com/beeware/toga/issues/1020).
        if future:
            future.set_result(None)

    def set_content(self, root_url, content):
        # There is a loadDataWithBaseURL method, but it's inconsistent about whether
        # getUrl returns the given URL or a data: URL. Rather than support this feature
        # intermittently, it's better to not support it at all.
        self.native.loadData(content, "text/html", "utf-8")

    def get_user_agent(self):
        return self.settings.getUserAgentString()

    def set_user_agent(self, value):
        self.settings.setUserAgentString(
            self.default_user_agent if value is None else value
        )

    def evaluate_javascript(self, javascript, on_result=None):
        result = JavaScriptResult(on_result)

        self.native.evaluateJavascript(javascript, ReceiveString(result))
        return result

    def set_on_navigation_starting(self, handler):
        # print(f"set_on_navigation_starting")
        pass

    def set_on_resource_requested(self, handler):
        # print(f"set_on_resource_requested")
        pass

    def cancel_navigation(self, navigation_event):
        navigation_event.cancel = True
 