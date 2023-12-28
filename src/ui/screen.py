import urwid

class Screen(urwid.WidgetWrap):
    def __init__(self, screen_manager):
        self.manager = screen_manager
        self.layout = self.create_layout()
        super().__init__(self.layout)

    # This enables the WidgetWrap to be focusable 
    # and receive keypress and other events
    def selectable(self):
        return True

    def create_layout(self):
        text = urwid.Text(u"404")
        filler = urwid.Filler(text, valign='top')
        return filler

    def keypress(self, size, key):
        if key == "esc":
            self.manager.go_back()
        
    def set_focus(self) -> None:
        self.layout.focus_position = 0