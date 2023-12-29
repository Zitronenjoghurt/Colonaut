import customtkinter as ctk
import src.ui.components as Components
from src.classes.event import Event
from src.classes.response import Response
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

        self.data_list = Components.DataList(self, [])
        self.data_list.grid(row=0, column=0, pady=(60, 0), padx=(10, 0), sticky="nw")

        self.action_buttons = ctk.CTkFrame(self, width=400, height=450)
        self.action_buttons.grid(row=1, column=0, sticky="sw", padx=(10,0), pady=(0, 60))
        self.action_buttons.grid_propagate(False)

        self.system_dashboard = Components.ShipSystemDashboard(self, {})
        self.system_dashboard.grid(row=0, column=2, rowspan=2, padx=(0,10), sticky="e")

        self.system_console = Components.ShipConsole(self, ["> please turn down your music", "> hello?", "> imma come to the bridge"])
        self.system_console.grid(row=0, column=1, rowspan=2, pady=125, sticky="nsew")

    def update_data(self) -> None:
        planet_data_event = Event(Event.TYPES.RETRIEVE_PLANET_DATA)
        ship_data_event = Event(Event.TYPES.RETRIEVE_SHIP_DATA)
        planet_data_response: Response = self.ui_system.publish_event(planet_data_event)
        ship_data_response: Response = self.ui_system.publish_event(ship_data_event)

        if planet_data_response.of_type(Response.TYPES.PLANET_DATA):
            planet_data = planet_data_response.get_data()
            self.data_list.update_data(planet_data)

        if ship_data_response.of_type(Response.TYPES.SHIP_DATA):
            ship_data = ship_data_response.get_data()
            self.system_dashboard.update_dashboard(ship_data)

    def jump(self) -> None:
        jump_event = Event(Event.TYPES.GAME_FLOW_JUMP)
        self.ui_system.publish_event(jump_event)
        self.update_data()

    def on_keypress(self, event) -> None:
        super().on_keypress(event)
        if event.keysym in ['j', 'J']:
            self.jump()