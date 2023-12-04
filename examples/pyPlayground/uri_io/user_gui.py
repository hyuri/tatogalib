import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from pyplayground import G, default_gui
from tatogalib.ui.window import TaWindow, TaGui
import tatogalib.ui.window as tawindow
from pathlib import Path
from platform import python_version
import sys
from mylib import system
from mylib.uri_io.urifilebrowser import UriFileBrowser
from mylib.uri_io.urifile import UriFile


class MainGui(TaGui):

    def __init__(self, app, parentGui, title, **kwargs):
        super().__init__(app, parentGui, title, **kwargs)
        self.message_area = None
        self.ti_source = None
        self.ti_target = None
    # __init__

    def build_gui(self):
        # create box for content
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=5, flex=1))

        if G.get_platform() == "windows":
            # adding commands
            self.app._impl._create_app_commands = G.create_app_commands  
            grpFile = toga.Group(text="File", order=1)
            # add actions
            cmdExit = toga.Command(
                lambda s: self.app.exit(),
                text="Exit",
                group=grpFile,
                section=sys.maxsize,
            )
            self.app.commands.add(cmdExit)

            cmdDebug = toga.Command(
                self.handle_debug,
                text="Show debug messages",
                group=grpFile,
                order=4,
            )
            self.app.commands.add(cmdDebug)
        # win32

        if G.get_platform() == "android":
            # Menu
            self.app.commands.clear()
            self.app._impl._create_app_commands = G.create_app_commands

            cmdDebug = toga.Command(
                self.handle_debug,
                text="Show debug messages",
                group=toga.Group.COMMANDS,
                order=40,
            )
            self.app.commands.add(cmdDebug)

        # add content to main_box
        btn_source = toga.Button("Source File", on_press=self.handle_btn_source)
        main_box.add(btn_source)
        self.ti_source = toga.TextInput(readonly=False, style=Pack(flex=1))
        main_box.add(self.ti_source)
        btn_target = toga.Button("Target File", on_press=self.handle_btn_target)
        main_box.add(btn_target)
        self.ti_target = toga.TextInput(readonly=False, style=Pack(flex=1))
        main_box.add(self.ti_target)
        btn_folder = toga.Button("Choose folder", on_press=self.handle_btn_folder)
        main_box.add(btn_folder)
        self.ti_folder = toga.TextInput(readonly=False, style=Pack(flex=1))
        main_box.add(self.ti_folder)
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
        main_box.add(self.message_area)
        # Button bar
        _button_box = toga.Box(style=Pack(direction=ROW))
        _button_box.add(toga.Label("", style=Pack(flex=1)))
        _button_box.add(toga.Button("Say hello", on_press=self.handle_btn_action))
        _button_box.add(toga.Button("Clear", on_press=self.handle_btn_clear))
        _button_box.add(toga.Label("", style=Pack(flex=1)))
        main_box.add(_button_box)
        return main_box
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
            self.fnPrintln(f"exists: {urifile.exists()}\n")
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
            uristring = self.ti_source.value
            urifile = UriFile(uristring)
            self.fnPrintln(f"name: {urifile.name}")
            self.fnPrintln(f"mime_type: {urifile.uristring}")
            self.fnPrintln(f"isdir: {urifile.isdir()}")
            self.fnPrintln(f"exists: {urifile.exists()}")
            self.fnPrintln(f"startup arguments: {str(system.get_startup_arguments())}\n")
            argv = system.get_startup_arguments()
            if len(argv) > 1:
                urifile = UriFile.from_path(Path(argv[1]))
                if urifile is not None:
                    self.fnPrintln(f"{argv[1]} = {urifile.get_uristring()}")
                else:
                    self.fnPrintln(f"{argv[1]} = None")

        except BaseException as ex:
            G.write_debug_message(str(ex))
            self.fnPrintln("\n" + str(ex))
    # handle_btn_action

    def handle_btn_clear(self, widget):
        self.message_area.value = ""
    # handle_btn_clear

    def handle_debug(self, widget):
        width = int(self.window.size[0]*0.9)
        height = int(self.window.size[1]*0.9)
        mygui = default_gui.DebugGui(self.app, self, "< Debug",
            size=(width, height),
        )
        mygui.show()
    # handle_drbug

    def fnPrint(self, message):
        self.message_area.value += message
    # fnPrint

    def fnPrintln(self, message):
        self.fnPrint(message + "\n")
    # fnPrintln

# MainGui
