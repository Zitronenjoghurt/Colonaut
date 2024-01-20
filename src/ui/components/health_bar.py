import customtkinter as ctk

class HealthBar(ctk.CTkProgressBar):
    def __init__(self, master, **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        self.default_fg_color = self.cget("fg_color")
        self.value = 0
        self.disabled = False

        self.disable()

    def set_health(self, value) -> None:
        self.enable()
        self.set(value)

        if value > 0.90:
            color = "dark green"
        elif value > 0.75:
            color = "green"
        elif value > 0.50:
            color = "yellow"
        elif value > 0.25:
            color = "orange"
        elif value > 0.1:
            color = "red"
        else:
            color = "dark red"

        self.configure(progress_color=color)

    def disable(self) -> None:
        if self.disabled:
            return
        
        self.disabled = True
        self.configure(fg_color="black")
        self.configure(progress_color="black")

    def enable(self) -> None:
        if not self.disabled:
            return
        
        self.disabled = False
        self.configure(fg_color=self.default_fg_color)
        self.set_health(self.value)