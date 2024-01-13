import customtkinter as ctk
from src.constants.locale_translator import LocaleTranslator
from src.events.event import Event
from src.events.event_bus import EventBus
from src.events.response import Response
from src.planet_generation.planet_image import PlanetImage

EVENT_BUS = EventBus.get_instance()
LT = LocaleTranslator.get_instance()

class PlanetReportWindow(ctk.CTkFrame):
    def __init__(self, master, height=800, width=950, **kwargs) -> None:
        super().__init__(master=master, height=height, width=width, **kwargs)
        self.pack_propagate(False)
        self.grid_propagate(False)

        primary_background = 'gray17'
        secondary_background = 'gray20'

        self.columnconfigure(0, weight=0, minsize=250)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0, minsize=50)
        self.rowconfigure(1, weight=0, minsize=250)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        self.close_button = ctk.CTkButton(self, fg_color="#bd2626", hover_color="#eb2d2d", text="X", font=("Geist Mono", 22, "bold"), width=30, height=30, command=self.on_exit)
        self.close_button.place(x=920, y=15)

        self.type_frame = ctk.CTkFrame(self, height=50, width=250)
        self.type_frame.grid_propagate(False)
        self.type_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=(25, 5))

        self.type_label = ctk.CTkLabel(self.type_frame, text="", font=("ELNATH", 22))
        self.type_label.pack(expand=True, fill='both', padx=5, pady=5)

        self.image_frame = ctk.CTkFrame(self, height=250, width=250)
        self.image_frame.grid_propagate(False)
        self.image_frame.grid(row=1, column=0, sticky="nsew", padx=25, pady=(5, 25))

        self.planet_image = ctk.CTkLabel(self.image_frame, text="", height=200, width=200)
        self.planet_image.pack(padx=25, pady=25)
    
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
    
    def on_exit(self) -> None:
        close_system_window = Event(Event.TYPES.UI_CLOSE_PLANET_REPORT_WINDOW)
        EVENT_BUS.publish(close_system_window)