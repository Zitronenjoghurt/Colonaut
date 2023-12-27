import urwid
import src.ui.screens as Screens
from typing import Optional

class UISystem():
    def __init__(self) -> None:
        self.loop: Optional[urwid.MainLoop] = None
        self.screens = {}
        self.history = []
        self.register_screens()

    def register_screens(self) -> None:
        self.screens["main_menu"] = Screens.MainMenuScreen(self)

    def set_screen(self, name) -> None:
        if self.loop is None:
            raise RuntimeError("Tried to change screen while ui loop was not running.")
        
        if name in self.screens:
            if self.loop.widget in self.screens.values():
                current_screen_name = [k for k, v in self.screens.items() if v == self.loop.widget][0]
                self.history.append(current_screen_name)

            self.loop.widget = self.screens[name]

    def go_back(self) -> None:
        if self.loop is None:
            raise RuntimeError("Tried to change screen while ui loop was not running.")
        
        if self.history:
            previous_screen = self.history.pop()
            self.loop.widget = self.screens[previous_screen]

    def start(self, initial_screen) -> None:
        self.loop = urwid.MainLoop(self.screens[initial_screen])
        self.loop.run()