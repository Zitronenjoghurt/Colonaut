import urwid

class Screen(urwid.WidgetWrap):
    def __init__(self, screen_manager):
        self.manager = screen_manager
        self.layout = self.create_layout()
        super().__init__(self.layout)

    def create_layout(self):
        text = urwid.Text(u"404")
        filler = urwid.Filler(text, valign='top')
        return filler

    def keypress(self, size, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()