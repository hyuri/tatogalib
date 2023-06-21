import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from pyplayground import G
from com.t_arn.pymod.ui.window import TaWindow, TaGui
import com.t_arn.pymod.ui.window as tawindow
from platform import python_version
import sys
from system.notification import Notification, NotificationManager, AppIcon


class MainGui(TaGui):
    main_box = None
    message_area = None
    _state_data = {}

    def __init__(self, app, parentGui, title, **kwargs):
        super().__init__(app, parentGui, title, **kwargs)
        self.noti_list = []

    # __init__

    def build_gui(self):
        # create box for content
        self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=5, flex=1))

        if G.get_platform() == "windows":
            # adding commands
            self.app.commands = toga.CommandSet(
                self.app.factory
            )  # replaces the default CommandSet
            # is there a better way to get rid of the default menu ?
            # File > Preferences, Exit
            # Help > About, Homepage
            # add actions
            grpFile = toga.Group(label="File", order=1)
            # add actions
            cmdExit = toga.Command(
                lambda s: self.app.exit(),
                label="Exit",
                group=grpFile,
                section=sys.maxsize,
            )
            self.app.commands.add(cmdExit)

            grpHelp = toga.Group(label="Help", order=3)
            cmdAbout = toga.Command(
                self.handle_commands, label="About", group=grpHelp, order=1
            )
            cmdAbout.id = "cmdAbout"
            self.app.commands.add(cmdAbout)
            cmdHelp = toga.Command(
                self.handle_commands, label="Help", group=grpHelp, order=2
            )
            cmdHelp.id = "cmdHelp"
            self.app.commands.add(cmdHelp)
            cmdHistory = toga.Command(
                self.handle_commands, label="History", group=grpHelp, order=3
            )
            cmdHistory.id = "cmdHistory"
            self.app.commands.add(cmdHistory)
            cmdDebug = toga.Command(
                self.handle_commands,
                label="Show debug messages",
                group=grpHelp,
                order=4,
            )
            cmdDebug.id = "cmdDebug"
            self.app.commands.add(cmdDebug)
        # win32

        if G.get_platform() == "android":
            # Menu
            self.app.commands = toga.CommandSet(
                self.app.factory
            )  # replaces the default CommandSet
            cmdAbout = toga.Command(
                self.handle_commands,
                label="About",
                group=toga.Group.COMMANDS,
                order=10,
            )
            cmdAbout.id = "cmdAbout"
            self.app.commands.add(cmdAbout)
            cmdHelp = toga.Command(
                self.handle_commands,
                label="Help",
                group=toga.Group.COMMANDS,
                order=20,
            )
            cmdHelp.id = "cmdHelp"
            self.app.commands.add(cmdHelp)
            cmdHistory = toga.Command(
                self.handle_commands,
                label="History",
                group=toga.Group.COMMANDS,
                order=30,
            )
            cmdHistory.id = "cmdHistory"
            self.app.commands.add(cmdHistory)
            cmdDebug = toga.Command(
                self.handle_commands,
                label="Show debug messages",
                group=toga.Group.COMMANDS,
                order=40,
            )
            cmdDebug.id = "cmdDebug"
            self.app.commands.add(cmdDebug)

        self.app.commands.add(
            toga.Command(
                self.post_notification_appicon,
                text="Post new notification (app icon)",
                group=toga.Group.COMMANDS,
                order=50,
            )
        )
        self.app.commands.add(
            toga.Command(
                self.post_notification_systemicon,
                text="Post new notification (system icon)",
                group=toga.Group.COMMANDS,
                order=51,
            )
        )
        self.app.commands.add(
            toga.Command(
                self.post_notification_customicon,
                text="Post new notification (custom icon)",
                group=toga.Group.COMMANDS,
                order=52,
            )
        )
        self.app.commands.add(
            toga.Command(
                self.cancel_notification,
                text="Cancel last notification",
                group=toga.Group.COMMANDS,
                order=55,
            )
        )
        self.app.commands.add(
            toga.Command(
                self.cancel_all_notifications,
                text="Cancel all notifications",
                group=toga.Group.COMMANDS,
                order=60,
            )
        )

        # add content to main_box
        self.message_area = toga.MultilineTextInput(
            value="", readonly=False, style=Pack(flex=1)
        )
        self.main_box.add(self.message_area)
        # Button bar
        _button_box = toga.Box(style=Pack(direction=ROW))
        _button_box.add(toga.Label("", style=Pack(flex=1)))
        _button_box.add(toga.Button("Say hello", on_press=self.handle_btn_action))
        _button_box.add(toga.Button("Clear", on_press=self.handle_btn_clear))
        _button_box.add(toga.Label("", style=Pack(flex=1)))
        self.main_box.add(_button_box)

    # build_gui

    def post_notification_appicon(self, widget):
        try:
            text = self.message_area.value
            self.fnPrintln("\nCreating Notification with app icon...")
            mgr = NotificationManager(self.fnPrintln)
            self.fnPrintln(f"Notifications enabled: {mgr.are_notifications_enabled()}")
            noti = Notification(
                "My title", text, None
            )
            id = mgr.post_notification(noti)
            self.fnPrintln(f"id: {id}, {noti.id}")
            self.noti_list.append(noti.id)
        except BaseException as ex:
            G.write_debug_message(str(ex))
            self.fnPrintln("\n" + str(ex))

    # post_notification_appicon

    def post_notification_systemicon(self, widget):
        try:
            text = self.message_area.value
            self.fnPrintln("\nCreating Notification with system icon...")
            mgr = NotificationManager(self.fnPrintln)
            self.fnPrintln(f"Notifications enabled: {mgr.are_notifications_enabled()}")
            noti = Notification(
                "My title", text, AppIcon.APP
            )
            id = mgr.post_notification(noti)
            self.fnPrintln(f"id: {id}, {noti.id}")
            self.noti_list.append(noti.id)
        except BaseException as ex:
            G.write_debug_message(str(ex))
            self.fnPrintln("\n" + str(ex))

    # post_notification_systemicon

    def post_notification_customicon(self, widget):
        try:
            text = self.message_area.value
            self.fnPrintln("\nCreating Notification with custom icon...")
            mgr = NotificationManager(self.fnPrintln)
            self.fnPrintln(f"Notifications enabled: {mgr.are_notifications_enabled()}")
            noti = Notification(
                "My title", text, str(self.app.paths.app / "resources" / "brutus.png")
            )
            id = mgr.post_notification(noti)
            self.fnPrintln(f"id: {id}, {noti.id}")
            self.noti_list.append(noti.id)
        except BaseException as ex:
            G.write_debug_message(str(ex))
            self.fnPrintln("\n" + str(ex))

    # post_notification_customicon

    def cancel_notification(self, widget):
        try:
            mgr = NotificationManager(self.fnPrintln)
            id = self.noti_list.pop()
            mgr.cancel_notification(id)
        except BaseException as ex:
            G.write_debug_message(str(ex))
            self.fnPrintln("\n" + str(ex))

    # cancel_notification

    def cancel_all_notifications(self, widget):
        try:
            mgr = NotificationManager(self.fnPrintln)
            mgr.cancel_all_notifications()
        except BaseException as ex:
            G.write_debug_message(str(ex))
            self.fnPrintln("\n" + str(ex))

    # cancel_all_notifications

    def handle_btn_action(self, widget):
        try:
            self.fnPrintln("Hello")
        except BaseException as ex:
            G.write_debug_message(str(ex))
            self.fnPrintln("\n" + str(ex))

    # handle_btn_action

    def handle_btn_clear(self, widget):
        self.message_area.clear()

    # handle_btn_clear

    def handle_commands(self, widget):
        if widget.id == "cmdAbout":
            mygui = AboutGui(self.app, self, "< About", size=(400, 300))
            return mygui.show()
        if widget.id == "cmdHelp":
            mygui = HtmlGui(
                self.app,
                self,
                "< Help",
                f"{G.programDir}/resources/help-en.html",
                size=(int(self.window.size[0] * 0.9), int(self.window.size[1] * 0.9)),
            )
            return mygui.show()
        if widget.id == "cmdHistory":
            mygui = HtmlGui(
                self.app,
                self,
                "< History",
                f"{G.programDir}/resources/history-en.html",
                size=(int(self.window.size[0] * 0.9), int(self.window.size[1] * 0.9)),
            )
            return mygui.show()
        if widget.id == "cmdDebug":
            return G.show_debug_messages()

    # handle_commands

    def fnPrint(self, message):
        self.message_area.value += message

    # fnPrint

    def fnPrintln(self, message):
        self.fnPrint(message + "\n")

    # fnPrintln

    # @override
    def restore_state(self):
        """
        This method is called after app restarted due to device rotation
        """
        if len(self._state_data) > 0:
            G.write_debug_message("Restoring app state")
            self.message_area.value = self._state_data["message_area"]
            G.write_debug_message(
                G.get_debug_messages() + "\n" + self._state_data["debug_messages"]
            )

    # restore_state

    # @override
    def save_state(self):
        """
        This method is called before app restarts when device rotation occurs
        All data saved to self._state_data is passed to the app on restart.
        """
        G.write_debug_message("Saving app state")
        self._state_data["message_area"] = self.message_area.value
        self._state_data["debug_messages"] = G.get_debug_messages()

    # save_state


# MainGui


class AboutGui(TaGui):
    window = None
    main_box = None
    message_area = None

    def __init__(self, app, parentGui, title, **kwargs):
        super().__init__(app, parentGui, title, **kwargs)

    # __init__

    def build_gui(self):
        # create box for content
        self.main_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        msg = f"Python Playground {G.objApp.version}\n\n"

        msg += "Freeware, (C) 2022 tanapro.ch\n\n"
        msg += "This software is based on\n"
        msg += f"Python {python_version()}\n"
        msg += f"Toga {toga.__version__}\n"
        msg += f"t_arn window {tawindow.version}\n\n"

        msg += "This app is a playground for Python developers who want to try Python "
        msg += "and Toga (www.beeware.org) without the need to set up a development environment "
        msg += "on the desktop with the complete toolchain.\n\n"

        msg += "To get started, read the help page of this app\n\n"

        msg += "The privacy policy can be found at\n"
        msg += "https://www.tanapro.ch/products/PrivacyPolicy/pyPlayground.html\n\n\n"

        if G.get_platform() == "android":
            msg += "\nPlatform: " + G.get_platform()
            vp = G.objMainGui.main_box._impl.container.viewport
            scale = float(vp.dpi) / vp.baseline_dpi
            msg += "\nViewport size in px: ({}, {})".format(vp.width, vp.height)
            msg += "\nViewport size in dp: ({}, {})".format(
                int(float(vp.width) / scale), int(float(vp.height) / scale)
            )
            msg += "\nDensityDPI: " + str(vp.dpi)
            msg += "\nScaling factor: " + str(scale)

        self.message_area = toga.MultilineTextInput(
            value=msg, readonly=True, style=Pack(flex=1)
        )
        self.main_box.add(self.message_area)

        # button bar
        _button_box = toga.Box(
            style=Pack(direction=ROW, padding=(5, 0, 0, 0))
        )  # top, right, bottom and left padding
        _button_box.add(toga.Label("", style=Pack(flex=1)))
        _button_box.add(toga.Button("OK", on_press=self.handle_btn_ok))
        _button_box.add(toga.Label("", style=Pack(flex=1)))
        self.main_box.add(_button_box)

    # build_gui

    def handle_btn_ok(self, widget):
        self.close()

    # handle_OK_button


# AboutGui


class HtmlGui(TaGui):
    window = None
    main_box = None
    _webView = None
    _html_text = None
    _html_file = None

    def __init__(self, app, parentGui, title, html_file, **kwargs):
        super().__init__(app, parentGui, title, **kwargs)
        self._html_file = html_file

    # __init__

    def build_gui(self):
        # create box for content
        self.main_box = toga.Box(style=Pack(direction=COLUMN, flex=1))
        # read help file
        self._html_file = self._html_file.replace("\\", "/")
        _f = open(self._html_file, "r", encoding="utf-8")
        _text = _f.read()
        _f.close()
        _text = _text.replace("{app_data_dir}", str(G.get_data_path()))
        self._webView = toga.WebView(style=Pack(flex=1))
        self._webView.set_content("data:text/html,", _text)
        self.main_box.add(self._webView)

        # button bar
        _button_box = toga.Box(
            style=Pack(direction=ROW, padding=(5, 0, 0, 0))
        )  # top, right, bottom and left padding
        _button_box.add(toga.Label("", style=Pack(flex=1)))
        _button_box.add(toga.Button("OK", on_press=self.handle_btn_ok))
        _button_box.add(toga.Label("", style=Pack(flex=1)))
        self.main_box.add(_button_box)

    # build_gui

    def handle_btn_ok(self, widget):
        self.close()

    # handle_btn_ok


# HtmlGui
