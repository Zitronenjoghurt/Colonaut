import customtkinter as ctk

class ShipConsole(ctk.CTkFrame):
    def __init__(self, master, height=800, width=950):
        super().__init__(master=master, height=height, width=width)
        self.pack_propagate(False)
        self.grid_propagate(False)

        console_frame = ctk.CTkFrame(self)
        console_frame.pack(expand=True, fill='both')

        self.console_text = ctk.CTkTextbox(console_frame, height=height, width=width, state='disabled', font=('Andale Mono', 22))
        self.console_text.pack(side='left', expand=True, fill='both')

        scrollbar = ctk.CTkScrollbar(console_frame, command=self.console_text.yview)
        scrollbar.pack(side='right', fill='y')

        self.console_text.configure(yscrollcommand=scrollbar.set)

        self.writing = False
        self.char_queue = []

    def write_texts(self, texts: list[str]) -> None:
        self.writing = True

        self.char_queue = []
        self.after_id = None
        for text in texts:
            self.queue_message("> "+ text)

    def append_message(self, message: str):
        self.console_text.configure(state='normal')
        self.console_text.insert('end', message)
        self.console_text.see('end')
        self.console_text.configure(state='disabled')

    def queue_message(self, message: str, delay=800, char_delay=25):
        for char in message + '\n':
            self.char_queue.append((char, char_delay))
        self.char_queue.append(('', delay))
        self.process_queue()

    def process_queue(self):
        if self.after_id is not None:
            return
        
        if not self.char_queue:
            self.writing = False
            return

        if self.char_queue:
            char, delay = self.char_queue.pop(0)
            self.append_message(char)
            self.after_id = self.after(delay, self.clear_after_id)

    def clear_after_id(self):
        self.after_id = None
        self.process_queue()