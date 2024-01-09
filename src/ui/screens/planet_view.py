import customtkinter as ctk
from typing import Optional
import src.ui.components as Components
from src.ui.dialogue import DialogueLibrary
from src.events.event import Event
from src.events.response import Response
from src.ui.screen import Screen

class PlanetViewScreen(Screen):
    def __init__(self, ui_system):
        super().__init__(ui_system=ui_system)
        # Grid layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.data_list = Components.DataList(self, [], width=400, height=450)
        self.data_list.grid(row=0, column=0, pady=(60, 0), padx=(10, 0), sticky="nw")

        self.can_jump = False
        self.action_buttons = ctk.CTkFrame(self, width=400, height=450)
        self.action_buttons.grid(row=1, column=0, sticky="sw", padx=(10,0), pady=(0, 60))
        self.action_buttons.grid_propagate(False)

        self.system_dashboard = Components.ShipSystemDashboard(self, {})
        self.system_dashboard.grid(row=0, column=2, rowspan=2, pady=(60, 60), padx=(15, 15), sticky="nsew")

        self.system_window = Components.SystemWindow(self)
        self.system_window.grid(row=0, column=1, rowspan=2, pady=60, sticky="nsew")

        self.ship_console = Components.ShipConsole(self)
        self.ship_console.grid(row=0, column=1, rowspan=2, pady=60, sticky="nsew")

        self.dialogue_library = DialogueLibrary.get_instance()

        self.default_fg_color = self.cget("fg_color")
        self.emergency = False

    def update_data(self) -> None:
        planet_data_event = Event(Event.TYPES.RETRIEVE_PLANET_DATA)
        ship_status_event = Event(Event.TYPES.RETRIEVE_SHIP_STATUS)
        planet_data_response: Response = self.ui_system.publish_event(planet_data_event)
        ship_status_response: Response = self.ui_system.publish_event(ship_status_event)

        planet_data = planet_data_response.get_data(Response.TYPES.PLANET_DATA)
        if planet_data:
            self.data_list.update_data(planet_data)

        ship_data = ship_status_response.get_data(Response.TYPES.SHIP_DATA)
        if ship_data:
            self.system_dashboard.update_dashboard(ship_data)

        ship_status_log = ship_status_response.get_data(Response.TYPES.SHIP_STATUS_LOG)
        if ship_status_log:
            self.ship_console.write_texts(ship_status_log)

    def update_system_dashboard(self) -> None:
        ship_status_event = Event(Event.TYPES.RETRIEVE_SHIP_STATUS)
        ship_status_response: Response = self.ui_system.publish_event(ship_status_event)
        ship_data = ship_status_response.get_data(Response.TYPES.SHIP_DATA)
        if ship_data:
            self.system_dashboard.update_dashboard(ship_data)

    def jump(self) -> None:
        if self.can_jump:
            self.can_jump = False
            jump_dialogue = self.dialogue_library.get_dialogue_by_name("ship_jump")
            self.ship_console.play_dialogue(dialogue=jump_dialogue)

            jump_event = Event(Event.TYPES.GAME_FLOW_JUMP)
            self.ui_system.publish_event(jump_event)

    def finish_jump(self) -> None:
        self.update_data()
        self.can_jump = True

    def on_keypress(self, event) -> None:
        super().on_keypress(event)
        if event.keysym in ['j', 'J']:
            self.jump()
            self.stop_emergency_animation()
    
    def start_console(self) -> None:
        self.ship_console.start_writing()

    def start_intro(self) -> None:
        intro_dialogue = self.dialogue_library.get_dialogue_by_name("intro")
        self.start_emergency_animation()
        self.ship_console.play_dialogue(intro_dialogue)

    def start_tutorial(self) -> None:
        tutorial_dialogue = self.dialogue_library.get_dialogue_by_name("tutorial")
        self.stop_emergency_animation()
        self.ship_console.clear()
        self.ship_console.play_dialogue(tutorial_dialogue)

    def start_game(self) -> None:
        self.can_jump = True
        self.ship_console.clear()

    def open_system_window(self, system_name: str, force_update: bool = False) -> None:
        self.system_window.update_data(system_name=system_name, force_update=force_update)
        self.system_window.lift()

    def close_system_window(self) -> None:
        self.ship_console.lift()

    def start_emergency_animation(self) -> None:
        self.emergency = True
        self.fade_to_red()

    def stop_emergency_animation(self) -> None:
        self.emergency = False
        self.configure(fg_color=self.default_fg_color)

    def fade_to_red(self, step=0):
        if not self.emergency:
            return
        if step <= 125:
            color = f"#%02x1111" % step  # Increment the red component
            self.configure(fg_color=color)
            self.after(10, lambda: self.fade_to_red(step + 1))
        else:
            self.fade_to_black()

    def fade_to_black(self, step=125):
        if not self.emergency:
            return
        if step >= 0:
            color = f"#%02x1111" % step  # Decrement the red component
            self.configure(fg_color=color)
            self.after(10, lambda: self.fade_to_black(step - 1))
        else:
            self.fade_to_red()