import customtkinter as ctk
from src.events.event import Event
from src.events.event_bus import EventBus

EVENT_BUS = EventBus.get_instance()

class PlanetReportWindow(ctk.CTkFrame):
    def __init__(self, master, height=800, width=950, **kwargs) -> None:
        super().__init__(master=master, height=height, width=width, **kwargs)
        self.pack_propagate(False)
        self.grid_propagate(False)

        primary_background = 'gray17'
        secondary_background = 'gray20'

        self.close_button = ctk.CTkButton(self, fg_color="#bd2626", hover_color="#eb2d2d", text="X", font=("Geist Mono", 22, "bold"), width=30, height=30, command=self.on_exit)
        self.close_button.place(x=920, y=15)
    
    def update_data(self) -> None:
        return
    
    def on_exit(self) -> None:
        close_system_window = Event(Event.TYPES.UI_CLOSE_PLANET_REPORT_WINDOW)
        EVENT_BUS.publish(close_system_window)