from __future__ import annotations

import asyncio
from typing import Any, Protocol

from toga.handlers import AsyncResult, OnResultT, wrapped_handler

# from .base import StyleT, Widget
from toga.widgets.base import StyleT, Widget

from ... import system


class JavaScriptResult(AsyncResult):
    RESULT_TYPE = "JavaScript"


class OnWebViewLoadHandler(Protocol):
    def __call__(self, widget: WebView, /, **kwargs: Any) -> object:
        """A handler to invoke when the WebView is loaded.

        :param widget: The WebView that was loaded.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """


if system.get_platform() == "windows":
    from .windows import taWebViewImpl
else:
    raise NotImplementedError(f"taWebView is not implemented for {system.get_platform()}")


#class WebView(Widget):
class taWebView(Widget):
    def __init__(
        self,
        id: str | None = None,
        style: StyleT | None = None,
        url: str | None = None,
        user_agent: str | None = None,
        on_navigation_starting=None,
        on_resource_requested=None,
        on_webview_load: OnWebViewLoadHandler | None = None,
    ):
        """Create a new WebView widget.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param url: The full URL to load in the WebView. If not provided,
            an empty page will be displayed.
        :param user_agent: The user agent to use for web requests. If not
            provided, the default user agent for the platform will be used.
        :param on_navigation_starting: A handler that will be invoked is raised when the 
            WebView is requesting permission to navigate or redirect to a different URI. 
        :param on_resource_requested: A handler that will be invoked when the 
            webview starts load (or reload)
        :param on_webview_load: A handler that will be invoked when the web view
            finishes loading.
        """
        super().__init__(id=id, style=style)

        # self._impl = self.factory.WebView(interface=self)
        self._impl =taWebViewImpl(interface=self)
        self.user_agent = user_agent

        # Set the load handler before loading the first URL.
        self.on_webview_load = on_webview_load
        self.on_navigation_starting = on_navigation_starting
        self.on_resource_requested = on_resource_requested
        self.url = url

    def _set_url(self, url: str | None, future: asyncio.Future | None) -> None:
        # Utility method for validating and setting the URL with a future.
        if (url is not None) and not url.startswith(("https://", "http://")):
            raise ValueError("WebView can only display http:// and https:// URLs")

        self._impl.set_url(url, future=future)

    @property
    def url(self) -> str | None:
        """The current URL, or ``None`` if no URL is currently displayed.

        After setting this property, it is not guaranteed that reading the property will
        immediately return the new value. To be notified once the URL has finished
        loading, use :any:`load_url` or :any:`on_webview_load`.
        """
        return self._impl.get_url()

    @url.setter
    def url(self, value: str | None) -> None:
        self._set_url(value, future=None)

    async def load_url(self, url: str) -> asyncio.Future:
        """Load a URL, and wait until the next :any:`on_webview_load` event.

        **Note:** On Android, this method will return immediately.

        :param url: The URL to load.
        """
        loop = asyncio.get_event_loop()
        loaded_future = loop.create_future()
        self._set_url(url, future=loaded_future)
        return await loaded_future

    @property
    def on_navigation_starting(self):
        """A handler that will be invoked is raised when the taWebView is requesting 
        permission to navigate or redirect to a different URI.
        Returns:
            The function ``callable`` that is called when the webview starts navigating.
        """
        return self._on_navigation_starting

    @on_navigation_starting.setter
    def on_navigation_starting(self, handler):
        """Set the handler to invoke when the webview starts navigating.

        :param handler (:obj:`callable`): The handler to invoke when the webview starts navigating.
            The handler will receive following arguments:
            widget: The taWebView instance
            url:    The URL to be navigated to
            event:  The native Event object
        """
        self._on_navigation_starting = wrapped_handler(self, handler)
        self._impl.set_on_navigation_starting(self._on_navigation_starting)

    @property
    def on_resource_requested(self):
        """The handler to invoke when the webview starts loading.
        Returns:
            The function ``callable`` that is called when the webview starts loading.
        """
        return self._on_resource_requested

    @on_resource_requested.setter
    def on_resource_requested(self, handler):
        """Set the handler to invoke when the webview starts loading.

        :param handler (:obj:`callable`): The handler to invoke when the webview starts loading.
        """
        self._on_resource_requested = wrapped_handler(self, handler)
        self._impl.set_on_resource_requested(self._on_resource_requested)

    @property
    def on_webview_load(self) -> OnWebViewLoadHandler:
        """The handler to invoke when the web view finishes loading.

        Rendering web content is a complex, multi-threaded process. Although a page
        may have completed *loading*, there's no guarantee that the page has been
        fully *rendered*, or that the widget representation has been fully updated.
        The number of load events generated by a URL transition or content change can
        be unpredictable. An ``on_webview_load`` event should be interpreted as an
        indication that some change has occurred, not that a *specific* change has
        occurred, or that a specific change has been fully propagated into the
        rendered content.

        **Note:** This is not currently supported on Android.
        """
        return self._on_webview_load

    @on_webview_load.setter
    def on_webview_load(self, handler: OnWebViewLoadHandler) -> None:
        if handler and not getattr(self._impl, "SUPPORTS_ON_WEBVIEW_LOAD", True):
            self.factory.not_implemented("WebView.on_webview_load")

        self._on_webview_load = wrapped_handler(self, handler)

    @property
    def user_agent(self) -> str:
        """The user agent to use for web requests.

        **Note:** On Windows, this property will return an empty string until the widget
        has finished initializing.
        """
        return self._impl.get_user_agent()

    @user_agent.setter
    def user_agent(self, value: str) -> None:
        self._impl.set_user_agent(value)

    def set_content(self, root_url: str, content: str) -> None:
        """Set the HTML content of the WebView.

        **Note:** On Android and Windows, the ``root_url`` argument is ignored. Calling
        this method will set the ``url`` property to ``None``.

        :param root_url: A URL which will be returned by the ``url`` property,
            and used to resolve any relative URLs in the content.
        :param content: The HTML content for the WebView
        """
        self._impl.set_content(root_url, content)

    def evaluate_javascript(
        self,
        javascript: str,
        on_result: OnResultT | None = None,
    ) -> JavaScriptResult:
        """Evaluate a JavaScript expression.

        **This is an asynchronous method**. There is no guarantee that the JavaScript
        has finished evaluating when this method returns. The object returned by this
        method can be awaited to obtain the value of the expression.

        **Note:** On Android and Windows, *no exception handling is performed*. If a
        JavaScript error occurs, a return value of None will be reported, but no
        exception will be provided.

        :param javascript: The JavaScript expression to evaluate.
        :param on_result: **DEPRECATED** ``await`` the return value of this method.
        """
        return self._impl.evaluate_javascript(javascript, on_result=on_result)

    def cancel_navigation(self, event):
        """Cancels the navigation being started

        :param object event: The `event` object received in the on_navigation_starting handler
        """
        self._impl.cancel_navigation(event)
