import urwid
from typing import Callable, Optional

def UIButton(label: str, on_press: Optional[Callable] = None, user_data = None, width: int = 20):
    button = urwid.Button(label=label)
    if on_press is not None:
        urwid.connect_signal(button, 'click', on_press, user_data)
    return urwid.Padding(button, width=width, align='center')