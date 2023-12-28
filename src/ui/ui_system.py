import urwid
import src.ui.screens as Screens
from typing import Optional
from ..classes.event import Event
from ..classes.event_subscriber import BaseEventSubscriber

class UISystem(BaseEventSubscriber):
    def __init__(self) -> None:
        self.loop: Optional[urwid.MainLoop] = None
        self.screens = {}
        self.history = []

        self.screens["main_menu"] = Screens.MainMenuScreen(self)
        self.screens["planet_view"] = Screens.PlanetViewScreen(self)

        self.SUBSCRIPTIONS = {
            Event.TYPES.UI_PUSH_PLANET_DATA: self.screens["planet_view"].update_planet_data
        }
        super().__init__()

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