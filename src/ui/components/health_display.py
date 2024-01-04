import customtkinter as ctk

class SystemHealthBar(ctk.CTkFrame):
    def __init__(self, master, system_name: str, health_percentage: float, width=200, height=20) -> None:
        super().__init__(master, width=width, height=height)
        self.pack_propagate(False)

        self.health_bar = ctk.CTkCanvas(self, bg='black', width=width, height=height, highlightthickness=0)
        self.health_bar.pack(fill='both', expand=True)

        self.health_percentage = health_percentage
        self.system_name = system_name
        self.width = width
        self.height = height

        self.draw_bar(self.health_percentage)

    def draw_bar(self, health_percentage):
        self.health_bar.delete("all")
        bar_length = self.width * health_percentage
        self.health_bar.create_rectangle(0, 0, bar_length, self.height, fill='darkgreen', width=0)
        self.health_bar.create_text(self.width / 2, self.height / 2, text=f"{self.system_name.capitalize()}", fill='white', font=('Geist Mono', 14))

    def update_health(self, new_health_percentage) -> None:
        self.health_percentage = new_health_percentage
        self.draw_bar(self.health_percentage)

class ShipSystemHealthDisplay(ctk.CTkFrame):
    def __init__(self, master, ship_data: list[tuple], width=200, height=500) -> None:
        super().__init__(master, width=width, height=height)
        self.pack_propagate(False)
        self.system_bars: dict[str, SystemHealthBar] = {}

        for system_name, system_health in ship_data:
            self.create_system_bar(system_name=system_name, system_health=system_health)

    def update_system_health(self, new_ship_data: list[tuple]) -> None:
        for system_name, system_health in new_ship_data:
            if system_name in self.system_bars:
                self.system_bars[system_name].update_health(system_health)
            else:
                self.create_system_bar(system_name=system_name, system_health=system_health)

    def create_system_bar(self, system_name: str, system_health: float) -> None:
        if system_name not in self.system_bars:
            system_bar = SystemHealthBar(self, system_name, system_health)
            system_bar.pack(fill='x', padx=10, pady=5)
            self.system_bars[system_name] = system_bar