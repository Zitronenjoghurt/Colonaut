from typing import Optional
from .config import Config

CONFIG = Config.get_instance()

class DisplayText:
    def __init__(self, text: str|list[str], tag: Optional[str] = None, char_delay: Optional[int] = None, line_delay: Optional[int] = None, newline: Optional[bool] = None, line_symbol: Optional[bool] = None) -> None:
        if tag is None:
            tag = CONFIG.DEFAULT_SHIP_CONSOLE_STYLE_TAG
        if char_delay is None:
            char_delay = CONFIG.DEFAULT_SHIP_CONSOLE_CHAR_DELAY
        if line_delay is None:
            line_delay = CONFIG.DEFAULT_SHIP_CONSOLE_LINE_DELAY
        if newline is None:
            newline = True
        if line_symbol is None:
            line_symbol = True

        if isinstance(text, list):
            self.texts = text
        else:
            self.texts = [text]

        self.texts = [str(text) for text in self.texts]
        self.tag = tag
        self.char_delay = char_delay
        self.line_delay = line_delay
        self.newline = newline
        self.line_symbol = line_symbol

    @staticmethod
    def from_dict(data) -> 'DisplayText':
        text = data.get("text", None)
        if text is None:
            raise ValueError("An error occured while initializing DisplayText: no text provided")
        tag = data.get("tag", None)
        char_delay = data.get("char_delay", None)
        line_delay = data.get("line_delay", None)
        newline = data.get("newline", None)
        line_symbol = data.get("line_symbol", None)
        return DisplayText(text=text, tag=tag, char_delay=char_delay, line_delay=line_delay, newline=newline, line_symbol=line_symbol)

    def add_text(self, text: str|list[str]) -> None:
        if isinstance(text, list):
            self.texts.extend(text)
        else:
            self.texts.append(text)

    def get_text(self) -> list[str]:
        return self.texts
    
    def do_newline(self) -> bool:
        return self.newline

    def do_line_symbol(self) -> bool:
        return self.line_symbol
    
    def get_options(self) -> dict:
        return {"tag": self.tag, "char_delay": self.char_delay, "line_delay": self.line_delay, "newline": self.newline}