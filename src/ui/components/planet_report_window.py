import customtkinter as ctk
from src.constants.locale_translator import LocaleTranslator
from src.events.event import Event
from src.events.event_bus import EventBus
from src.events.response import Response
from .habitability_box import HabitabilityBox

EVENT_BUS = EventBus.get_instance()
LT = LocaleTranslator.get_instance()

class PlanetReportWindow(ctk.CTkFrame):
    def __init__(self, master, height=800, width=950, **kwargs) -> None:
        super().__init__(master=master, height=height, width=width, **kwargs)
        self.pack_propagate(False)
        self.grid_propagate(False)

        self.columnconfigure(0, weight=0, minsize=250)
        self.columnconfigure(1, weight=0, minsize=250)
        self.columnconfigure(2, weight=0, minsize=250)
        self.columnconfigure(3, weight=0, minsize=250)
        self.rowconfigure(0, weight=0, minsize=50)
        self.rowconfigure(1, weight=0, minsize=250)
        self.rowconfigure(2, weight=0, minsize=300)
        self.rowconfigure(3, weight=0, minsize=300)

        self.close_button = ctk.CTkButton(self, fg_color="#bd2626", hover_color="#eb2d2d", text="X", font=("Geist Mono", 22, "bold"), width=30, height=30, command=self.on_exit)
        self.close_button.place(x=920, y=15)

        type_frame = ctk.CTkFrame(self, height=50, width=250)
        type_frame.grid_propagate(False)
        type_frame.grid(row=0, column=0, sticky="nsew", padx=(25, 5), pady=(25, 5))

        self.type_label = ctk.CTkLabel(type_frame, text="", font=("ELNATH", 22))
        self.type_label.pack(expand=True, fill='both', padx=5, pady=5)

        type_description_frame = ctk.CTkFrame(self, height=300, width=250)
        type_description_frame.grid_propagate(False)
        type_description_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 5), pady=(25, 5), rowspan=2)

        self.type_description = ctk.CTkLabel(type_description_frame, text="", font=("Geist Mono", 18), justify='left', wraplength=250)
        self.type_description.pack(expand=True, fill='x', padx=15, pady=15, anchor="n")

        image_frame = ctk.CTkFrame(self, height=250, width=250)
        image_frame.grid_propagate(False)
        image_frame.grid(row=1, column=0, sticky="nsew", padx=(25, 5), pady=(5, 5))

        self.planet_image = ctk.CTkLabel(image_frame, text="", height=200, width=200)
        self.planet_image.pack(padx=25, pady=25)

        habitability_frame = ctk.CTkFrame(self, height=600, width=250)
        habitability_frame.grid_propagate(False)
        habitability_frame.grid(row=2, column=0, rowspan=2, sticky="nsew", padx=(25, 5), pady=(5, 25))

        self.temperature_box = HabitabilityBox(habitability_frame)
        self.temperature_box.pack(fill='x', padx=10, pady=(15, 10), anchor='n')

        self.gravity_box = HabitabilityBox(habitability_frame)
        self.gravity_box.pack(fill='x', padx=10, pady=10, anchor='n')
        
        # placeholder for the future
        self.whatever_box = HabitabilityBox(habitability_frame)
        self.whatever_box.pack(fill='x', padx=10, pady=(10, 15), anchor='n')

        atmosphere_frame = ctk.CTkFrame(self, height=300, width=250)
        atmosphere_frame.grid_propagate(False)
        atmosphere_frame.grid(row=2, column=1, sticky="nsew", padx=(5, 5), pady=(5, 5))

        resource_frame = ctk.CTkFrame(self, height=300, width=250)
        resource_frame.grid_propagate(False)
        resource_frame.grid(row=3, column=1, sticky="nsew", padx=(5, 5), pady=(5, 25))
    
    def update_data(self) -> None:
        planet_report_event = Event(Event.TYPES.RETRIEVE_PLANET_REPORT)
        planet_report_response = EVENT_BUS.publish(planet_report_event)
        planet_report = planet_report_response.get_data(Response.TYPES.PLANET_REPORT)

        if not planet_report:
            return
        
        image: ctk.CTkImage = planet_report.get("image", None)
        if isinstance(image, ctk.CTkImage):
            self.planet_image.configure(image=image)
        type: str = planet_report.get("type", None)
        if isinstance(type, str):
            self.type_label.configure(text=LT.get(type))
            self.type_description.configure(text=LT.get(type+"_description"))
    
    def on_exit(self) -> None:
        close_system_window = Event(Event.TYPES.UI_CLOSE_PLANET_REPORT_WINDOW)
        EVENT_BUS.publish(close_system_window)