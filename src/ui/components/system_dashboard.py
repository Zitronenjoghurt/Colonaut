import customtkinter as ctk
from src.constants.locale_translator import LocaleTranslator
from src.events.event import Event
from src.events.event_bus import EventBus
from src.ui.components.health_bar import HealthBar

EVENT_BUS = EventBus.get_instance()
LT = LocaleTranslator.get_instance()

class Panel(ctk.CTkFrame):
    def __init__(self, master, system_name: str, health_percentage: float, additional_data: list[tuple], height=125, width=150):
        super().__init__(master, height=height, width=width, fg_color='gray17')
        self.system_name = system_name

        self.pack_propagate(False)
        self.grid_propagate(False)

        # Also propagating the mouse enter and leave events from the child widgets
        # ensures that theres no funny business when leaving the panel with the mouse
        
        name_label = ctk.CTkLabel(self, text=LT.get(system_name), font=('Geist Mono', 12))
        name_label.pack(pady=(1,0))

        self.health_bar = HealthBar(self)
        self.health_bar.pack(fill='x', padx=15)
        self.health_bar.set_health(health_percentage)

        additional_text = []
        for key, value in additional_data:
            additional_text.append(f"{LT.get(key)}: {value}")
        
        if additional_text:
            additional_text_label = ctk.CTkLabel(self, text='\n'.join(additional_text))
            additional_text_label.bind("<Enter>", self.on_mouse_enter)
            additional_text_label.bind("<Leave>", self.on_mouse_leave)
            additional_text_label.bind("<Button-1>", self.on_mouse_click)
            additional_text_label.pack()

        name_label.bind("<Enter>", self.on_mouse_enter)
        name_label.bind("<Leave>", self.on_mouse_leave)
        name_label.bind("<Button-1>", self.on_mouse_click)
        self.health_bar.bind("<Enter>", self.on_mouse_enter)
        self.health_bar.bind("<Leave>", self.on_mouse_leave)
        self.health_bar.bind("<Button-1>", self.on_mouse_click)
        self.bind("<Enter>", self.on_mouse_enter)
        self.bind("<Leave>", self.on_mouse_leave)
        self.bind("<Button-1>", self.on_mouse_click)

    def on_mouse_enter(self, event) -> None:
        self.configure(fg_color='gray25')

    def on_mouse_leave(self, event) -> None:
        self.configure(fg_color='gray17')

    def on_mouse_click(self, event) -> None:
        system_window_event = Event(Event.TYPES.UI_OPEN_SYSTEM_WINDOW, system_name=self.system_name)
        EVENT_BUS.publish(system_window_event)

class ShipSystemDashboard(ctk.CTkFrame):
    def __init__(self, master, systems_data, height=900, width=480):
        super().__init__(master, height=height, width=width)
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.systems_data = systems_data
        self.create_dashboard()

    def create_dashboard(self):
        row = 0
        column = 0
        for system_name, data in self.systems_data.items():
            health = data.get('health', 0)
            additional_data = [(k, v) for k, v in data.items() if k != 'health']

            panel = Panel(self, system_name, health, additional_data)
            panel.grid(row=row, column=column, sticky="nsew", padx=5, pady=5)

            column += 1
            if column >= 3:
                column = 0
                row += 1

    def update_dashboard(self, new_data):
        for child in self.winfo_children():
            child.destroy()

        self.systems_data = new_data
        self.create_dashboard()