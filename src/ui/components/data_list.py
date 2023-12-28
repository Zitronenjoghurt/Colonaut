import urwid

class DataList(urwid.Pile):
    def __init__(self, data):
        super().__init__(self.create_list(data))
    
    def create_list(self, data: list[tuple]):
        if len(data) == 0:
            return []
        
        rows = []
        label_width = max(len(label) for label, _ in data) + 2

        for label, value in data:
            row = urwid.Columns([
                (label_width, urwid.Text(f'{label}:')),
                urwid.Text(str(value))
            ])
            rows.append(row)

        return rows
    
    def update_data(self, new_data: list[tuple]) -> None:
        new_contents = self.create_list(new_data)
        self.contents.clear()
        for widget in new_contents:
            self.contents.append((widget, self.options('pack')))