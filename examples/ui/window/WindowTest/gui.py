import sys
from threading import Timer
import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack
from tatogalib.util import appconfig
from tatogalib.ui.window import TaGui
from tatogalib.util.i18nUtils import I18nUtils


_ = None
config = None
i18n = None


def get_platform():
    return toga.platform.current_platform
# get_platform


class MainGui(TaGui):

    def __init__(self, app, parentGUI, title, **kwargs):
        global _, config, i18n
        self.message_area = None
        super().__init__(app, parentGUI, title, **kwargs)
        _config_default = {'lang': 'en', 'font_size': 14}
        config = appconfig.read_config(app.paths.config, _config_default)
        i18n = I18nUtils(app.paths.app / "resources/i18n" , "en", lang=config["lang"])
        _ = i18n.t  # shortcut for translate method
    # __init__

    def create_app_commands(self):
        # do nothing because we do not want the default commands
        pass

    def build_gui(self) -> toga.Widget:
        top_box = toga.Box(style=Pack(flex=1, direction=COLUMN, padding=5))
        self.app._impl._create_app_commands = self.create_app_commands  # disable default commands
        if get_platform() == "windows":
            # adding commands
            # add actions
            grpFile = toga.Group(text=_("File"), order=1)
            # add actions
            cmdSettings = toga.Command(
                self.settings, text=_("Settings"), group=grpFile,
            )
            self.app.commands.add(cmdSettings)
            cmdExit = toga.Command(
                lambda s: self.app.exit(),
                text=_("Exit"),
                group=grpFile,
                section=sys.maxsize,
            )
            self.app.commands.add(cmdExit)

            grpHelp = toga.Group(text=_("Help"), order=3)
            cmdAbout = toga.Command(
                self.about, text=_("About"), group=grpHelp, order=1
            )
            self.app.commands.add(cmdAbout)
        # win32

        if get_platform() == "android":
            # Menu
            cmdSettings = toga.Command(
                self.settings,
                text=_("Settings"),
                group=toga.Group.COMMANDS,
                order=10,
            )
            self.app.commands.add(cmdSettings)
            cmdAbout = toga.Command(
                self.about,
                text=_("About"),
                group=toga.Group.COMMANDS,
                order=20,
                section=sys.maxsize
            )
            self.app.commands.add(cmdAbout)
        mti_message = toga.MultilineTextInput(placeholder=_("Enter_some_text_here"), style=Pack(flex=1))
        top_box.add(mti_message)
        if get_platform() == "windows":
            # auto-closing windows are not supported on Android
            top_box.add(toga.Button("Auto-closing window", on_press=self.auto_closing_window))
        return top_box
    # build_gui

    def about(self, widget):
        html_text = _("AboutContent")
        gui = WebViewGui(self.app, self, "About window", html_text)
        gui.show()
    # about

    def auto_closing_window(self, widget):
        gui = AutoClosingGui(self.app, self, "Auto-Closing Window", auto_close_duration=5.5)
        gui.show()
    # auto_closing_window

    def settings(self, widget):
        gui = SettingsGui(self.app, self, "Settings Window")
        gui.show()

# MainGui


class AutoClosingGui(TaGui):

    def __init__(self, app, parentGui, title, ok_button=True, **kwargs):
        self.auto_close_duration = None
        if "size" not in kwargs or (kwargs["size"] is None):
            kwargs["size"] = (int(parentGui.window.size[0]*0.8), int(parentGui.window.size[1]*0.8))
        if "position" not in kwargs or (kwargs["position"] is None):
            kwargs["position"] = None
        if "auto_close_duration" in kwargs:
            self.auto_close_duration = kwargs["auto_close_duration"]
        super().__init__(app, parentGui, title, **kwargs)
        self._ok_button = ok_button
    # __init__

    def build_gui(self) -> toga.Widget:
        # create box for content
        top_box = toga.Box(style=Pack(flex=1, direction=COLUMN))
        top_box.add(toga.Label(_("This_window_will_auto_close_in_x_seconds", duration=self.auto_close_duration)))
        # commands
        if get_platform() == "android":
            self.app.commands.clear()
            cmdBack = toga.Command(
                self.handle_ok_button,
                text=_("Back"),
                group=toga.Group.COMMANDS,
                order=10,
            )
            self.app.commands.add(cmdBack)

        # button bar
        if self._ok_button is True:
            box_buttons = toga.Box(
                style=Pack(direction=ROW, padding=(5, 0, 0, 0))
            )  # top, right, bottom and left padding
            box_buttons.add(toga.Label("", style=Pack(flex=1)))
            box_buttons.add(toga.Button("OK", on_press=self.handle_ok_button))
            box_buttons.add(toga.Label("", style=Pack(flex=1)))
            top_box.add(box_buttons)
        return top_box
    # build_gui

    def handle_ok_button(self, widget):
        self.close()
    # handle_ok_button

# AutoClosingGui


class SettingsGui(TaGui):

    def __init__(self, app, parentGui, title, **kwargs):
        self._dd_lang = None
        self._ti_font_size = None
        if "size" not in kwargs or (kwargs["size"] is None):
            kwargs["size"] = (300, 200)
        super().__init__(app, parentGui, title, **kwargs)
    # __init__

    def build_gui(self) -> toga.Widget:
        # create box for content
        top_box = toga.Box(style=Pack(flex=1, direction=COLUMN, padding=5))

        # commands
        if get_platform() == "android":
            self.app.commands.clear()
            cmdBack = toga.Command(
                self.handle_cancel_button,
                text=_("Back"),
                group=toga.Group.COMMANDS,
                order=10,
            )
            self.app.commands.add(cmdBack)

        # lang
        lang_box = toga.Box(style=Pack(direction=ROW, padding=5))
        lang_box.add(
            toga.Label(
                _("Language"),
                style=Pack(font_size=config["font_size"], width=200, padding_right=8),
            )
        )
        self._dd_lang = toga.Selection(
            items=i18n.get_app_languages(),
            style=Pack(font_size=config["font_size"], flex=1),
        )
        self._dd_lang.value = config["lang"]
        lang_box.add(self._dd_lang)
        top_box.add(lang_box)
        # font_size
        box_font_size = toga.Box(style=Pack(direction=ROW, padding=5))
        box_font_size.add(
            toga.Label(
                _("Font_size"),
                style=Pack(font_size=config["font_size"], width=200, padding_right=8),
            )
        )
        self._ti_font_size = toga.TextInput(
            style=Pack(font_size=config["font_size"], flex=1)
        )
        self._ti_font_size.value = config["font_size"]
        box_font_size.add(self._ti_font_size)
        top_box.add(box_font_size)

        # button bar
        box_buttons = toga.Box(
            style=Pack(direction=ROW, padding=(5, 0, 0, 0))
        )  # top, right, bottom and left padding
        box_buttons.add(toga.Label("", style=Pack(flex=1)))
        box_buttons.add(
            toga.Button(
                _("Save"),
                on_press=self.handle_save_button,
                style=Pack(font_size=config["font_size"]),
            )
        )
        box_buttons.add(
            toga.Button(
                _("Cancel"),
                on_press=self.handle_cancel_button,
                style=Pack(font_size=config["font_size"]),
            )
        )
        box_buttons.add(toga.Label("", style=Pack(flex=1)))
        top_box.add(box_buttons)
        return top_box
    # build_gui

    def handle_cancel_button(self, widget):
        self.close()
    # handle_cancel_button

    async def handle_save_button(self, widget):
        config["lang"] = self._dd_lang.value
        config["font_size"] = int(self._ti_font_size.value)
        appconfig.write_config(self.app.paths.config, config)
        self.app.main_window.info_dialog("Info", _("You_need_to_restart_to_apply_settings"))
        self.close()
    # handle_ok_button
# SettingsGui


class WebViewGui(TaGui):

    def __init__(self, app, parentGui, title, html_text=None, ok_button=True, **kwargs):
        self._webView = None
        if "size" not in kwargs or (kwargs["size"] is None):
            kwargs["size"] = (300, 200)
        if "position" not in kwargs or (kwargs["position"] is None):
            kwargs["position"] = None
        super().__init__(app, parentGui, title, **kwargs)
        self._html_text = html_text
        self._ok_button = ok_button
    # __init__

    def build_gui(self) -> toga.Widget:
        # create box for content
        top_box = toga.Box(style=Pack(flex=1, direction=COLUMN))
        self._webView = toga.WebView(style=Pack(flex=1))
        self._webView.set_content("", self._html_text)
        top_box.add(self._webView)

        # commands
        if get_platform() == "android":
            self.app.commands.clear()
            cmdBack = toga.Command(
                self.handle_ok_button,
                text=_("Back"),
                group=toga.Group.COMMANDS,
                order=10,
            )
            self.app.commands.add(cmdBack)

        # button bar
        if self._ok_button is True:
            box_buttons = toga.Box(
                style=Pack(direction=ROW, padding=(5, 0, 0, 0))
            )  # top, right, bottom and left padding
            box_buttons.add(toga.Label("", style=Pack(flex=1)))
            box_buttons.add(toga.Button("OK", on_press=self.handle_ok_button))
            box_buttons.add(toga.Label("", style=Pack(flex=1)))
            top_box.add(box_buttons)
        return top_box
    # build_gui

    def handle_ok_button(self, widget):
        self.close()
    # handle_ok_button
# WebViewGui
