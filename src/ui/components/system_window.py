import customtkinter as ctk
from src.events.event import Event
from src.events.event_bus import EventBus
from src.events.response import Response
from .data_list import DataList

EVENT_BUS = EventBus.get_instance()

class SystemWindow(ctk.CTkFrame):
    def __init__(self, master, height=800, width=950, **kwargs):
        super().__init__(master=master, height=height, width=width, **kwargs)
        self.pack_propagate(False)
        self.grid_propagate(False)

        primary_background = 'gray17'
        secondary_background = 'gray20'

        self.system_label = ctk.CTkLabel(self, text="SYSTEM", font=("ELNATH", 30, "bold"))
        self.system_label.pack(pady=(25, 0))

        self.close_button = ctk.CTkButton(self, fg_color="red", text="X", font=("Geist Mono", 22, "bold"), width=30, height=30, command=self.on_exit)
        self.close_button.place(x=930, y=15)

        description_frame = ctk.CTkFrame(self, width=900, height=150)
        description_frame.pack(pady=(25,0))

        self.description = ctk.CTkLabel(description_frame, text="", font=("Geist Mono", 16), wraplength=900, justify='left')
        self.description.pack(pady=10, padx=10, expand=True, fill='both')

        information_frame = ctk.CTkFrame(self, width=900, height=150, fg_color=secondary_background)
        information_frame.columnconfigure(0, weight=1, minsize=460)
        information_frame.columnconfigure(1, weight=1, minsize=460)
        information_frame.rowconfigure(0, weight=1)
        information_frame.rowconfigure(1, weight=5)
        information_frame.pack(pady=(25,0))
        
        stats_label = ctk.CTkLabel(information_frame, text='STATS', font=("ELNATH", 24, "bold"), fg_color=secondary_background)
        stats_label.grid(column=0, row=0, sticky='nsew')

        stats_frame = ctk.CTkFrame(information_frame, fg_color=primary_background)
        stats_frame.grid(column=0, row=1, sticky='nsew', pady=10, padx=(0, 10))

        self.stats = DataList(master=stats_frame, data=[], font_size=24, font_weight='bold')
        self.stats.pack(pady=10, padx=10, expand=True, fill='both')

        additional_info_label = ctk.CTkLabel(information_frame, text='ADDITIONAL INFORMATION', font=("ELNATH", 24, "bold"), fg_color=secondary_background)
        additional_info_label.grid(column=1, row=0)

        additional_info_frame = ctk.CTkFrame(information_frame, fg_color=primary_background)
        additional_info_frame.grid(column=1, row=1, sticky='nsew', pady=10, padx=(10, 0))

        self.additional_info = ctk.CTkLabel(additional_info_frame, text="", font=("Geist Mono", 16), wraplength=410, justify='left')
        self.additional_info.pack(pady=10, padx=10, expand=True, fill='both')

    def update_data(self, system_name: str) -> None:
        system_data_event = Event(Event.TYPES.RETRIEVE_SYSTEM_WINDOW_DATA, system_name=system_name)
        system_data_response = EVENT_BUS.publish(system_data_event)
        system_data = system_data_response.get_data(Response.TYPES.SYSTEM_WINDOW_DATA)

        description = system_data.get("description", None)
        stats = system_data.get("stats", None)

        self.system_label.configure(text=system_name.upper())

        if not isinstance(description, str):
            description = "ERROR: INVALID DESCRIPTION"
        
        if not isinstance(stats, list):
            stats = []
        
        self.description.configure(text=description)
        self.stats.update_data(new_data=stats)

    def on_exit(self) -> None:
        close_system_window = Event(Event.TYPES.UI_CLOSE_SYSTEM_WINDOW)
        EVENT_BUS.publish(close_system_window)