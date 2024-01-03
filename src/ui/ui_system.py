import tkinter as tk
import src.ui.screens as Screens
from tkinter import messagebox
from ..classes.event import Event
from ..classes.event_subscriber import BaseEventSubscriber
from ..classes.response import Response

class UISystem(BaseEventSubscriber):
    def __init__(self) -> None:
        self.width = 1920
        self.height = 1080

        self.root = tk.Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.title("Colonaut")

        self.root.protocol("WM_DELETE_WINDOW", self.on_quit)
        self.root.bind("<Key>", self.on_keypress)

        self.screens = {}
        self.history = []
        self.can_go_back = True

        self.screens["main_menu"] = Screens.MainMenuScreen(self)
        self.screens["planet_view"] = Screens.PlanetViewScreen(self)

        for screen in self.screens.values():
            screen.place(x=0, y=0, relwidth=1.0, relheight=1.0)
        
        # Show main menu
        self.current_screen = "main_menu"
        self.screens["main_menu"].lift()
        
        subscriptions = {
            Event.TYPES.UI_START_PLANET_VIEW_EMERGENCY: self.on_activate_planet_view_emergency,
            Event.TYPES.UI_STOP_PLANET_VIEW_EMERGENCY: self.on_deactivate_planet_view_emergency
        }

        super().__init__(subscriptions=subscriptions)

    def switch_screen(self, screen_name: str, add_to_history: bool = True) -> None:
        if self.current_screen == screen_name:
            return
        
        if add_to_history and self.current_screen not in self.history:
            self.history.append(self.current_screen)
        
        self.screens[screen_name].lift()
        self.current_screen = screen_name

    def go_back(self) -> None:
        if self.can_go_back and self.history:
            last_screen = self.history.pop()
            self.switch_screen(last_screen, False)
    
    def on_quit(self) -> None:
        if messagebox.askyesno(title="Quit?", message="Do you really want to quit the game?"):
            self.root.destroy()

    def on_keypress(self, event):
        self.screens[self.current_screen].on_keypress(event)

    def start(self, mode: str = "") -> None:
        match mode:
            case "intro":
                self.screens["planet_view"].start_intro()

        self.root.mainloop()

    def start_ship_console(self) -> None:
        self.screens["planet_view"].start_console()

    """
    Event functions which alter the UI
    """
    def on_activate_planet_view_emergency(self) -> Response:
        self.screens["planet_view"].start_emergency_animation()
        return Response.create()
    
    def on_deactivate_planet_view_emergency(self) -> Response:
        self.screens["planet_view"].stop_emergency_animation()
        return Response.create()