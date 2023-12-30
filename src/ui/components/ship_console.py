import tkinter as tk
import customtkinter as ctk
from src.classes.display_text import DisplayText
from ..style_tags import StyleTags

class ShipConsole(ctk.CTkFrame):
    def __init__(self, master, height=800, width=950):
        super().__init__(master=master, height=height, width=width)
        self.pack_propagate(False)
        self.grid_propagate(False)

        console_frame = ctk.CTkFrame(self)
        console_frame.pack(expand=True, fill='both')

        self.console_text = ctk.CTkTextbox(console_frame, height=height, width=width, state='disabled', font=('Andale Mono', 22))
        self.console_text.pack(side='left', expand=True, fill='both')
        self.init_style_tags()

        scrollbar = ctk.CTkScrollbar(console_frame, command=self.console_text.yview)
        scrollbar.pack(side='right', fill='y')

        self.console_text.configure(yscrollcommand=scrollbar.set)

        self.writing = False
        self.after_id = None
        self.char_queue = []

    def init_style_tags(self) -> None:
        for config in StyleTags.TAGS:
            font = config.get("font", None)
            if font:
                config["font"] = ctk.CTkFont(**font)
            self.console_text._textbox.tag_config(**config)

    def write_texts(self, display_texts: list[DisplayText]) -> None:
        for display_text in display_texts:
            self.write_text(display_text=display_text)

    def write_text(self, display_text: DisplayText) -> None:
        self.writing = True

        for text_data in display_text.get_texts():
            message = text_data.get("text", None)
            tag = text_data.get("tag", None)
            line_delay = text_data.get("line_delay", None)
            char_delay = text_data.get("char_delay", None)
            newline = text_data.get("newline", None)
            if message is None or tag is None:
                raise RuntimeError("An error occured while trying to display a message.")
            self.queue_message(message=message, tag=tag, line_delay=line_delay, char_delay=char_delay, newline=newline)

    def append_message(self, message: str, tag: str = "computer"):
        self.console_text.configure(state='normal')
        self.console_text.insert('end', message, tag)
        self.console_text.see('end')
        self.console_text.configure(state='disabled')

    def queue_message(self, message: str, tag: str, line_delay=800, char_delay=25, newline=False):
        if newline:
            message += '\n'
        for char in message:
            self.char_queue.append((char, tag, char_delay))
        self.char_queue.append(('', tag, line_delay))
        self.process_queue()

    def process_queue(self):
        if self.after_id is not None:
            return
        
        if not self.char_queue:
            self.writing = False
            self.after_id = None
            return
    
        if self.char_queue:
            char, tag, delay = self.char_queue.pop(0)
            self.append_message(char, tag)
            self.after_id = self.after(delay, self.clear_after_id)

    def clear_after_id(self):
        self.after_id = None
        self.process_queue()