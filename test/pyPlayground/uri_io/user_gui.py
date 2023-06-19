import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from pyplayground import G
from com.t_arn.pymod.ui.window import TaWindow, TaGui
import com.t_arn.pymod.ui.window as tawindow
from platform import python_version
import sys
from uri_io.urifilebrowser import UriFileBrowser
from uri_io.urifile import UriFile


class MainGui(TaGui):
    main_box = None
    message_area = None
    _state_data = {}
    ti_source = None
    ti_target = None

    def __init__(self, app, parentGui, title, **kwargs):
        super().__init__(app, parentGui, title, **kwargs)

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

        # add content to main_box
        btn_source = toga.Button("Source File", on_press=self.handle_btn_source)
        self.main_box.add(btn_source)
        self.ti_source = toga.TextInput(readonly=False, style=Pack(flex=1))
        self.main_box.add(self.ti_source)
        btn_target = toga.Button("Target File", on_press=self.handle_btn_target)
        self.main_box.add(btn_target)
        self.ti_target = toga.TextInput(readonly=False, style=Pack(flex=1))
        self.main_box.add(self.ti_target)
        btn_folder = toga.Button("Choose folder", on_press=self.handle_btn_folder)
        self.main_box.add(btn_folder)
        self.ti_folder = toga.TextInput(readonly=False, style=Pack(flex=1))
        self.main_box.add(self.ti_folder)
        # commands for testing uri_io
        uri_group = toga.command.Group(
            text="uri_io", parent=toga.Group.COMMANDS, order=50
        )
        self.app.commands.add(
            toga.Command(
                self.handle_read,
                text="Read text from source file",
                group=uri_group,
                order=10,
            )
        )
        self.app.commands.add(
            toga.Command(
                self.handle_copy,
                text="Copy file",
                group=uri_group,
                order=20,
            )
        )
        self.app.commands.add(
            toga.Command(
                self.handle_delete,
                text="Delete source file",
                group=uri_group,
                order=30,
            )
        )
        self.app.commands.add(
            toga.Command(
                self.handle_write,
                text="Write text to target file",
                group=uri_group,
                order=40,
            )
        )
        self.app.commands.add(
            toga.Command(
                self.handle_persist_access,
                text="Persist access to target file",
                group=uri_group,
                order=50,
            )
        )
        self.app.commands.add(
            toga.Command(
                self.handle_listdir,
                text="List folder content",
                group=uri_group,
                order=60,
            )
        )
        self.app.commands.add(
            toga.Command(
                self.handle_createfile,
                text="Create a file in folder",
                group=uri_group,
                order=70,
            )
        )
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

    async def handle_btn_source(self, widget):
        try:
            fb = UriFileBrowser(self.fnPrintln)
            # initial = "content://com.android.externalstorage.documents/document/primary%3A!Daten"
            initial = "file:///C:/Projects/Python/_Docs"
            urilist = await fb.open_file_dialog(
                "Wähle eine Quellen Datei",
                file_types=["xlsx", "pdf", "rar"],
                multiselect=True,
                initial_uri=initial,
            )
            if len(urilist) == 0:
                return
            self.ti_source.value = str(urilist[0])
            urifile = UriFile(urilist[0], fnLog=self.fnPrintln)
            self.fnPrintln("")
            self.fnPrintln(f"name: {urifile.name}")
            self.fnPrintln(f"mime_type: {urifile.mime_type}")
            self.fnPrintln(f"size: {urifile.size}")
        except BaseException as ex:
            G.write_debug_message(str(ex))
            self.fnPrintln("\n" + str(ex))

    # handle_btn_source

    async def handle_btn_target(self, widget):
        try:
            fb = UriFileBrowser(self.fnPrintln)
            uristring = await fb.save_file_dialog(
                "Wähle eine Ziel Datei", "test.pdf", file_types=["xls", "pdf", "txt"]
            )
            self.ti_target.value = str(uristring)
            if uristring is None:
                return
            urifile = UriFile(uristring)
            self.fnPrintln("")
            self.fnPrintln(f"name: {urifile.name}")
            self.fnPrintln(f"exists: {urifile.exists()}")
            self.fnPrintln(f"isfile: {urifile.isfile()}")
            if urifile.isfile():
                self.fnPrintln(f"size: {urifile.size}")
        except BaseException as ex:
            G.write_debug_message(str(ex))
            self.fnPrintln("\n" + str(ex))

    # handle_btn_target

    def handle_copy(self, widget):
        try:
            source = UriFile(self.ti_source.value, fnLog=self.fnPrintln)
            target = UriFile(self.ti_target.value, fnLog=self.fnPrintln)
            self.fnPrint("\nCopying...")
            ok = source.copy_to(target)
            self.fnPrintln(f"done, ok={ok}")
            ok = target.set_lastmodified(source.lastmodified)
            self.fnPrint(f"Setting last modification time: {ok}")
        except BaseException as ex:
            G.write_debug_message(str(ex))
            self.fnPrintln("\n" + str(ex))

    # handle_copy

    def handle_delete(self, widget):
        self.fnPrint("\nDeleting...")
        source = UriFile(self.ti_source.value, fnLog=self.fnPrintln)
        ok = source.delete()
        self.fnPrintln(f"done, ok={ok}")

    # handle_delete

    async def handle_btn_folder(self, widget):
        try:
            fb = UriFileBrowser(self.fnPrintln)
            initial = "content://com.android.externalstorage.documents/document/primary%3A!Daten"
            # initial = "file:///C:/Program%20Files"
            uri = await fb.select_folder_dialog(
                "Wähle ein Verzeichnis", initial_uri=initial
            )
            self.fnPrintln("")
            self.fnPrintln(str(uri))
            if uri is None:
                return
            self.ti_folder.value = str(uri)
            urifile = UriFile(uri)
            self.fnPrintln(f"name: {urifile.name}")
            self.fnPrintln(f"mime_type: {urifile.mime_type}")
            self.fnPrintln(f"isdir: {urifile.isdir()}")
            self.fnPrintln(f"exists: {urifile.exists()}")
        except BaseException as ex:
            G.write_debug_message(str(ex))
            self.fnPrintln("\n" + str(ex))

    # handle_btn_folder

    def handle_read(self, widget):
        try:
            source = UriFile(self.ti_source.value, fnLog=self.fnPrintln)
            self.fnPrint("\nReading...")
            f = source.open("rt", "utf-8-sig")
            bytesobj = f.read()
            self.fnPrintln("read ok")
            f.close()
            self.fnPrintln(f"done")
            self.fnPrintln(str(bytesobj))
            for b in bytesobj:
                self.fnPrint(f"{ord(b)} ")
        except BaseException as ex:
            G.write_debug_message(str(ex))
            self.fnPrintln("\n" + str(ex))

    # handle_read

    def handle_write(self, widget):
        try:
            text = self.message_area.value
            target = UriFile(self.ti_target.value, fnLog=self.fnPrintln)
            self.fnPrintln("\nOpen for writing...")
            f = target.open("wt", "utf-8", "\r\n")
            self.fnPrintln("Writing...")
            size = f.write(text)
            self.fnPrintln(f"{size} chars written")
            self.fnPrintln("Closing...")
            f.close()
            self.fnPrintln("Done!")
        except BaseException as ex:
            G.write_debug_message(str(ex))
            self.fnPrintln("\n" + str(ex))

    # handle_write

    def handle_persist_access(self, widget):
        try:
            target = UriFile(self.ti_target.value, fnLog=self.fnPrintln)
            self.fnPrintln("\nPersisting access...")
            target.request_persistent_access()
            self.fnPrintln("Done!")
        except BaseException as ex:
            G.write_debug_message(str(ex))
            self.fnPrintln("\n" + str(ex))

    # handle_persist_access

    def handle_listdir(self, widget):
        try:
            folder = UriFile(self.ti_folder.value, fnLog=self.fnPrintln)
            children = folder.listdir()
            if children is None:
                self.fnPrintln("Uri is not a folder")
            for urifile in children:
                self.fnPrintln(f"\nname: {urifile.name}")
                self.fnPrintln(f"mime_type: {urifile.mime_type}")
                self.fnPrintln(f"uristring: {urifile.uristring}")
                self.fnPrintln(f"isdir: {urifile.isdir()}")
                self.fnPrintln(f"exists: {urifile.exists()}")
        except BaseException as ex:
            G.write_debug_message(str(ex))
            self.fnPrintln("\n" + str(ex))

    # handle_listdir

    def handle_createfile(self, widget):
        try:
            self.fnPrintln("\nCreating new file...")
            folder = UriFile(self.ti_folder.value, fnLog=self.fnPrintln)
            urifile = folder.create_file("new_file.abc", replace=True)
            if urifile is None:
                self.fnPrintln("None")
                return
            self.fnPrintln(f"name: {urifile.name}")
            self.fnPrintln(f"mime_type: {urifile.mime_type}")
            self.fnPrintln(f"uristring: {urifile.uristring}")
        except BaseException as ex:
            G.write_debug_message(str(ex))
            self.fnPrintln(f"\n{type(ex).__name__}: {str(ex)}")

    # handle_createfile

    def handle_btn_action(self, widget):
        try:
            self.fnPrintln("Hello")
            uristring = self.ti_folder.value
            urifile = UriFile(uristring)
            self.fnPrintln(f"name: {urifile.name}")
            self.fnPrintln(f"mime_type: {urifile.uristring}")
            self.fnPrintln(f"isdir: {urifile.isdir()}")
            self.fnPrintln(f"exists: {urifile.exists()}")

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
