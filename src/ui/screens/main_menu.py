import urwid
from src.ui.components import UIButton
from src.ui.screen import Screen

class MainMenuScreen(Screen):
    def __init__(self, screen_manager):
        super().__init__(screen_manager=screen_manager)

    def create_layout(self):
        title_text = urwid.BigText("COLONAUT", urwid.HalfBlock5x4Font())
        title_text = urwid.Padding(title_text, 'center', width='clip')
        divider = urwid.Divider(top=4)

        menu_text = ["Start Game", "Options", "Exit"]
        menu_items = [urwid.AttrMap(UIButton(text, self.on_menu_item_selected, width=15), None, focus_map='reversed') for text in menu_text]

        combined_widgets = [title_text, divider] + menu_items

        menu_pile = urwid.Pile(combined_widgets)
        menu_filler = urwid.Filler(menu_pile, valign='middle')
        return menu_filler
    
    def keypress(self, size, key):
        if key == "esc":
            raise urwid.ExitMainLoop()
        
    def on_menu_item_selected(self, button_label):
        match button_label.label:
            case "Start Game":
                self.manager.set_screen("planet_view")
            case "Options":
                pass
            case "Exit":
                raise urwid.ExitMainLoop()