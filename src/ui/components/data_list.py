import customtkinter as ctk

class DataList(ctk.CTkFrame):
    def __init__(self, master, data: list[tuple], font_family='Geist Mono', font_size=18, font_weight="normal", **kwargs):
        super().__init__(master, **kwargs)
        self.pack_propagate(False)
        self.grid_propagate(False)
        
        self.metrics_label = ctk.CTkLabel(self, anchor='w', font=(font_family, font_size, font_weight), justify='left')
        self.data_label = ctk.CTkLabel(self, anchor='w', font=(font_family, font_size, font_weight), justify='left')
        self.update_data(data)

    def update_data(self, new_data):
        metrics_text = "\n".join(label+":" for label, _ in new_data)
        data_text = "\n".join(value for _, value in new_data)

        self.metrics_label.configure(text=metrics_text)
        self.data_label.configure(text=data_text)

        self.metrics_label.pack(side='left', padx=5, pady=5, anchor='n')
        self.data_label.pack(side='left', padx=5, pady=5, anchor='n')