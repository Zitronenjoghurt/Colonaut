import tkinter as tk
import customtkinter as ctk
from src.ui.screen import Screen

class MainMenuScreen(Screen):
    def __init__(self, ui_system):
        super().__init__(ui_system=ui_system)
        self.title_text = ctk.CTkLabel(master=self, text="COLONAUT", font=('ELNATH', 80))
        self.title_text.pack(pady=(100, 0))

        self.inspired_by = ctk.CTkLabel(master=self, text="inspired by Seedship", font=('ELNATH', 15))
        self.inspired_by.pack()

        self.btn_start_game = ctk.CTkButton(master=self, text="Start Game", font=("Geist Mono", 20, "bold"), command=self.start_game)
        self.btn_start_game.pack(pady=(50, 0))

        self.btn_options = ctk.CTkButton(master=self, text="Options", font=("Geist Mono", 20, "bold"))
        self.btn_options.pack(pady=(25, 0))

        self.btn_quit = ctk.CTkButton(master=self, text="Quit", font=("Geist Mono", 20, "bold"), command=self.ui_system.on_quit)
        self.btn_quit.pack(pady=(25, 0))

    def start_game(self) -> None:
        self.ui_system.switch_screen("planet_view")
        self.ui_system.start_ship_console()

    def on_keypress(self, event) -> None:
        if event.keysym == "Escape":
            self.ui_system.on_quit()