import urwid
from src.ui.components import UIButton
from src.ui.screen import Screen

class MainMenuScreen(Screen):
    def __init__(self, screen_manager):
        super().__init__(screen_manager=screen_manager)

    def create_layout(self):
        menu_text = ["Start Game", "Options", "Exit"]
        menu_items = [urwid.AttrMap(UIButton(text, self.on_menu_item_selected, width=15), None, focus_map='reversed') for text in menu_text]

        menu_pile = urwid.Pile(menu_items)
        menu_filler = urwid.Filler(menu_pile, valign='middle')
        return menu_filler

    def on_menu_item_selected(self, button_label):
        match button_label.label:
            case "Start Game":
                pass
            case "Options":
                pass
            case "Exit":
                raise urwid.ExitMainLoop()