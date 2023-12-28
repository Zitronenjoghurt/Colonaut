import tkinter as tk
import customtkinter as ctk

class Screen(ctk.CTkFrame):
    def __init__(self, ui_system):
        super().__init__(master=ui_system.root, width=ui_system.width, height=ui_system.height)
        self.ui_system = ui_system

    def on_keypress(self, event) -> None:
        if event.keysym == "Escape":
            self.ui_system.go_back()