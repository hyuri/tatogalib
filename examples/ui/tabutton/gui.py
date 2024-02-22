import random

import toga
from toga.colors import BLUE, RED
from toga.constants import COLUMN, ROW
from toga.style import Pack
from tatogalib.ui.tabutton import TaButton
from tatogalib.ui.window import TaGui
from pyplayground import GM


# class ExampleButtonApp(toga.App):
class MainGui(TaGui):
    # def startup(self):
    def build_gui(self):
        # self.main_window = toga.MainWindow(
        #     size=(800, 500), resizable=False, minimizable=False
        # )

        # Common style of the inner boxes
        style_inner_box = Pack(direction=COLUMN)

        # Button class
        #   Simple button with text and callback function called when
        #   hit the button
        button1 = TaButton(
            "Change Text",
            on_press=self.callback_text,
            style=Pack(flex=1),
        )

        # Button with text and enable option
        # Keep a reference to it so it can be enabled by another button.
        self.button2 = TaButton(
            "Button is disabled!",
            enabled=False,
            style=Pack(flex=1),
            on_press=self.callback_disable,
        )

        # Button with text and style option
        button3 = TaButton("Bigger", style=Pack(width=200))

        # Button with text and callback function called
        button4a = TaButton("Make window larger", on_press=self.callback_larger)
        button4b = TaButton("Make window smaller", on_press=self.callback_smaller)

        # Box class
        # Container of components
        #   Add components for the first row of the outer box
        inner_box1 = toga.Box(
            style=style_inner_box,
            children=[
                button1,
                self.button2,
                button3,
                button4a,
                button4b,
            ],
        )

        # Button with text and margin style
        button5 = TaButton("Far from home", style=Pack(padding=50, color=BLUE))

        # Button with text and RGB color
        button6 = TaButton("RGB : Fashion", style=Pack(background_color=RED))

        # Button with text and string color
        button7 = TaButton("String : Fashion", style=Pack(background_color=BLUE))

        # Button with text and string color
        button8 = TaButton(
            "Big Font",
            style=Pack(font_family="serif", font_size=20, font_weight="bold"),
        )

        # Button with icon
        button9 = TaButton(
            icon=toga.Icon(GM.get_data_path() / "button_example/resources/star"),
        )
        button10 = TaButton(
            None, 
            icon=None,
        )
        icon = toga.Icon(GM.get_data_path() / "button_example/resources/star")
        button10.set_icon(icon, 30)
        button11 = TaButton(
            None, 
            icon=None,
        )
        icon = toga.Icon(GM.get_data_path() / "button_example/resources/star")
        button11.set_icon(icon, 60)

        # Add components for the second row of the outer box
        inner_box2 = toga.Box(
            style=style_inner_box,
            children=[button5, button6, button7, button8, button9, button10, button11],
        )

        #  Create the outer box with 2 rows
        outer_box = toga.Box(
            style=Pack(direction=ROW), children=[inner_box1, inner_box2]
        )

        # Add the content on the main window
        # self.main_window.content = outer_box

        # Show the main window
        # self.main_window.show()
        return outer_box

    def callback_text(self, button):
        # Some action when you hit the button
        #   In this case the text will change
        button.text = f"Magic {random.randint(0, 100)}!!"

        # If the disabled button isn't enabled, enable it.
        if not self.button2.enabled:
            self.button2.enabled = True
            self.button2.text = "Disable button"

    def callback_disable(self, button):
        button.enabled = False
        button.text = "Button is disabled!"

    def callback_larger(self, button):
        # Some action when you hit the button
        #   In this case the window size will change
        # self.main_window.size = (1000, 600)
        self.app.main_window.info_dialog("Info", "Window cannot be made larger")

    def callback_smaller(self, button):
        # Some action when you hit the button
        #   In this case the window size will change
        # self.main_window.size = (200, 200)
        self.app.main_window.info_dialog("Info", "Window cannot be made smaller")

