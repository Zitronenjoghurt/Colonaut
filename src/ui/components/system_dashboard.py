import customtkinter as ctk
from .health_bar import HealthBar

class Panel(ctk.CTkFrame):
    def __init__(self, master, system_name: str, health_percentage: float, additional_data: list[tuple], height=125, width=150):
        super().__init__(master, height=height, width=width)
        self.pack_propagate(False)
        self.grid_propagate(False)

        ctk.CTkLabel(self, text=system_name, font=('Geist Mono', 16)).pack()

        self.health_bar = HealthBar(self)
        self.health_bar.pack(fill='x', padx=15)
        self.health_bar.set_health(health_percentage)

        additional_text = []
        for key, value in additional_data:
            additional_text.append(f"{key}: {value}")
            
        if additional_text:
            ctk.CTkLabel(self, text='\n'.join(additional_text)).pack()

class ShipSystemDashboard(ctk.CTkFrame):
    def __init__(self, master, systems_data, height=750, width=480):
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