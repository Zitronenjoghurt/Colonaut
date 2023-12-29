import customtkinter as ctk

class ShipConsole(ctk.CTkFrame):
    def __init__(self, master, texts: list[str], height=800, width=950):
        super().__init__(master=master, height=height, width=width)
        self.pack_propagate(False)
        self.grid_propagate(False)

        console_frame = ctk.CTkFrame(self)
        console_frame.pack(expand=True, fill='both')

        self.console_text = ctk.CTkTextbox(console_frame, height=height, width=width, state='disabled', font=('Andale Mono', 22), yscrollcommand=True)
        self.console_text.pack(side='left', expand=True, fill='both')

        scrollbar = ctk.CTkScrollbar(console_frame, command=self.console_text.yview)
        scrollbar.pack(side='right', fill='y')

        self.console_text.configure(yscrollcommand=scrollbar.set)

        for text in texts:
            self.append_message(text)

    def append_message(self, message: str):
        self.console_text.configure(state='normal')
        self.console_text.insert('end', message + '\n')
        self.console_text.see('end')
        self.console_text.configure(state='disabled')