import customtkinter as ctk
from typing import Optional
from src.classes.display_text import DisplayText
from src.classes.dialogue import Dialogue
from src.ui.style_tags import StyleTags

class ShipConsole(ctk.CTkFrame):
    def __init__(self, master, height=800, width=950, **kwargs):
        super().__init__(master=master, height=height, width=width, **kwargs)
        self.pack_propagate(False)
        self.grid_propagate(False)

        console_frame = ctk.CTkFrame(self)
        console_frame.pack(expand=True, fill='both')

        self.current_dialogue: Optional[Dialogue] = None

        self.button_frame = ctk.CTkFrame(self, bg_color='systemWindowBackgroundColor')

        # Initialize buttons
        self.action1 = ctk.CTkButton(self.button_frame, command=lambda:self.dialogue_action(1))
        self.action2 = ctk.CTkButton(self.button_frame, command=lambda:self.dialogue_action(2))
        self.action3 = ctk.CTkButton(self.button_frame, command=lambda:self.dialogue_action(3))
        self.action4 = ctk.CTkButton(self.button_frame, command=lambda:self.dialogue_action(4))
        self.action1.grid(row=0, column=0, sticky='NSEW', padx=15, pady=15)
        self.action2.grid(row=0, column=1, sticky='NSEW', padx=15, pady=15)
        self.action3.grid(row=0, column=2, sticky='NSEW', padx=15, pady=15)
        self.action4.grid(row=0, column=3, sticky='NSEW', padx=15, pady=15)

        self.action_buttons = [self.action1, self.action2, self.action3, self.action4]
        self.current_actions = []
        
        # Hide buttons
        self.action1.grid_remove()
        self.action2.grid_remove()
        self.action3.grid_remove()
        self.action4.grid_remove()

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

    def play_dialogue(self, dialogue: Dialogue) -> None:
        self.current_dialogue = dialogue
        self.write_texts(dialogue.get_texts())

    def dialogue_action(self, action_id: int) -> None:
        if self.current_dialogue is None:
            raise RuntimeError("Dialogue action triggered but there is no dialogue.")
        action_name = self.current_actions[action_id - 1]
        answer = self.current_dialogue.get_action_answer(action_name=action_name)
        self.write_text(answer)
        self.current_dialogue.process_action(action_name=action_name)
        self.write_texts(self.current_dialogue.get_texts())
        self.reset_dialogue_actions()

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
        
        # Finished writing
        if not self.char_queue:
            self.after_id = None
            self.on_finish_writing()
            return
    
        if self.char_queue:
            char, tag, delay = self.char_queue.pop(0)
            self.append_message(char, tag)
            self.after_id = self.after(delay, self.clear_after_id)

    def clear_after_id(self):
        self.after_id = None
        self.process_queue()

    def set_dialogue_actions(self, labels: list[str]) -> None:
        self.current_actions = labels
        self.init_actions(labels=labels)
        self.show_action_frame()

    def reset_dialogue_actions(self) -> None:
        self.current_actions = []
        self.hide_action_frame()
        self.reset_actions()

    def hide_action_frame(self) -> None:
        self.button_frame.pack_forget()
    
    def show_action_frame(self) -> None:
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)
        self.button_frame.columnconfigure(3, weight=1)
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.pack(expand=True, fill='both')

    def reset_actions(self) -> None:
        for button in self.action_buttons:
            button.configure(text="")
            button.grid_remove()

    def init_action(self, action_id: int, label: str) -> None: 
        if action_id < 1 or action_id > len(self.action_buttons):
            raise RuntimeError(f"Invalid action id {action_id} for action button labeled {label}. There are only {len(self.action_buttons)} available action buttons.")
        button = self.action_buttons[action_id - 1]
        button.configure(text=label)
        button.grid()

    def init_actions(self, labels: list[str]) -> None:
        for i, label in enumerate(labels):
            self.init_action(action_id=i+1, label=label)

    def on_finish_writing(self) -> None:
        self.writing = False
        if self.current_dialogue:
            if self.current_dialogue.waiting_for_action():
                self.set_dialogue_actions(self.current_dialogue.get_action_labels())
            if self.current_dialogue.is_finished():
                self.current_dialogue = None