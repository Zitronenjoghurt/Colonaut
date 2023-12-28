import customtkinter as ctk

class DataList(ctk.CTkFrame):
    def __init__(self, master, data: list[tuple]):
        super().__init__(master)
        self.metrics_label = ctk.CTkLabel(self, anchor='w', font=('Helvetica Neue', 14), justify='left')
        self.data_label = ctk.CTkLabel(self, anchor='w', font=('Helvetica Neue', 14), justify='left')
        self.update_data(data)

    def update_data(self, new_data):
        metrics_text = "\n".join(label+":" for label, _ in new_data)
        data_text = "\n".join(value for _, value in new_data)

        self.metrics_label.configure(text=metrics_text)
        self.data_label.configure(text=data_text)

        self.metrics_label.pack(side='left', fill='y', padx=5, pady=5)
        self.data_label.pack(side='left', fill='y', padx=5, pady=5)