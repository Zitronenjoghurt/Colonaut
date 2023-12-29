import customtkinter as ctk

class HealthBar(ctk.CTkProgressBar):
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master=master, **kwargs)

    def set_health(self, value) -> None:
        self.set(value)

        if value > 0.75:
            color = "dark green"
        elif value > 0.50:
            color = "yellow"
        elif value > 0.25:
            color = "orange"
        else:
            color = "red"

        self.configure(progress_color=color)