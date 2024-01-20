import customtkinter as ctk
from typing import Optional
from .health_bar import HealthBar

class HabitabilityBox(ctk.CTkFrame):
    def __init__(self, master, title="", height=180, width=240, fg_color='gray14', **kwargs) -> None:
        super().__init__(master=master, height=height, width=width, fg_color=fg_color, **kwargs)
        self.pack_propagate(False)
        self.grid_propagate(False)

        self.title_label = ctk.CTkLabel(self, text=title.upper(), font=("GeoFont", 16, "bold"))
        self.title_label.pack(fill="x")

        self.non_habitation = ctk.CTkLabel(self, text="without habitation:", font=("GeoFont", 14), anchor="w")
        self.non_habitation.pack(fill='x', pady=(5, 0), padx=10)

        self.non_habitation_bar = HealthBar(self)
        self.non_habitation_bar.pack(fill='x', padx=10)

        self.with_habitation = ctk.CTkLabel(self, text="with habitation:", font=("GeoFont", 14), anchor="w")
        self.with_habitation.pack(fill='x', pady=(20, 0), padx=10)

        self.with_habitation_bar = HealthBar(self)
        self.with_habitation_bar.pack(fill='x', padx=10)

    def update_data(self, non_percentage: Optional[float] = None, with_percentage: Optional[float] = None) -> None:
        if non_percentage is None or with_percentage is None:
            self.disable()
            return

        self.non_habitation_bar.set_health(non_percentage / 100)
        self.with_habitation_bar.set_health(with_percentage / 100)

    def disable(self) -> None:
        self.non_habitation_bar.disable()
        self.with_habitation_bar.disable()