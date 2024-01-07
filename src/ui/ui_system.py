import tkinter as tk
import customtkinter as ctk
import tkinter.font as tkFont
import src.ui.screens as Screens
from tkinter import messagebox
from src.constants.custom_fonts import REGULAR_FONT_REGISTRY, BOLD_FONT_REGISTRY
from src.events.event import Event
from src.events.event_subscriber import BaseEventSubscriber
from src.events.response import Response

class UISystem(BaseEventSubscriber):
    def __init__(self) -> None:
        self.width = 1920
        self.height = 1080
        ctk.set_appearance_mode("dark")

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
            Event.TYPES.UI_CLOSE_SYSTEM_WINDOW: self.close_system_window,
            Event.TYPES.UI_OPEN_SYSTEM_WINDOW: self.open_system_window,
            Event.TYPES.UI_START_PLANET_VIEW_EMERGENCY: self.on_activate_planet_view_emergency,
            Event.TYPES.UI_STOP_PLANET_VIEW_EMERGENCY: self.on_deactivate_planet_view_emergency,
            Event.TYPES.UI_UPDATE_SYSTEM_DASHBOARD: self.update_system_dashboard
        }

        self.check_custom_fonts_installed()

        super().__init__(subscriptions=subscriptions)

    @staticmethod
    def check_custom_fonts_installed() -> None:
        available_fonts = tkFont.families()
        for font in REGULAR_FONT_REGISTRY:
            if font not in available_fonts:
                raise RuntimeError(f"Missing font: '{font}'\nLook up the project's fonts folder and check if you have installed all necessary fonts.")
        for font in BOLD_FONT_REGISTRY:
            bold_font = tkFont.Font(family=font, size=12, weight="bold")
            actual_weight = bold_font.actual()["weight"]
            if actual_weight != "bold":
                raise RuntimeError(f"Missing font: bold variant of '{font}'\nLook up the project's fonts folder and check if you have installed all necessary fonts.")

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
                self.start_intro()
            case "tutorial":
                self.start_tutorial()
            case "game":
                self.start_gameplay()

        self.root.mainloop()

    def start_intro(self) -> None:
        self.screens["planet_view"].start_intro()

    def start_tutorial(self) -> None:
        self.screens["planet_view"].start_tutorial()

    def start_gameplay(self) -> None:
        self.screens["planet_view"].start_game()

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
    
    def open_system_window(self, system_name: str, force_update: bool = False) -> Response:
        self.screens["planet_view"].open_system_window(system_name=system_name, force_update=force_update)
        return Response.create()

    def close_system_window(self) -> Response:
        self.screens["planet_view"].close_system_window()
        return Response.create()
    
    def update_system_dashboard(self) -> Response:
        self.screens["planet_view"].update_system_dashboard()
        return Response.create()