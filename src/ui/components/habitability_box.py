import customtkinter as ctk
from .health_bar import HealthBar

class HabitabilityBox(ctk.CTkFrame):
    def __init__(self, master, height=180, width=240, fg_color='gray14', **kwargs) -> None:
        super().__init__(master=master, height=height, width=width, fg_color=fg_color, **kwargs)
        self.pack_propagate(False)
        self.grid_propagate(False)