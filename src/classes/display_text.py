from typing import Optional
from .config import Config

CONFIG = Config.get_instance()

class DisplayText:
    CHARACTER_SPACES = {
        "energy": 0,
        "nexus": 0,
        "sensor": 0
    }

    def __init__(self, text: str|list[str], character: Optional[str] = None, tag: Optional[str] = None, char_delay: Optional[int] = None, line_delay: Optional[int] = None, line_symbol: Optional[bool] = None, newline: Optional[bool] = None) -> None:
        if tag is None:
            tag = CONFIG.DEFAULT_SHIP_CONSOLE_STYLE_TAG
        if char_delay is None:
            char_delay = CONFIG.DEFAULT_SHIP_CONSOLE_CHAR_DELAY
        if line_delay is None:
            line_delay = CONFIG.DEFAULT_SHIP_CONSOLE_LINE_DELAY
        if line_symbol is None:
            line_symbol = True
        if newline is None:
            newline = True

        if character and character not in self.CHARACTER_SPACES:
            raise ValueError(f"Character {character} does not exist.")
        elif character:
            character = character.lower() 

        if isinstance(text, list):
            self.texts = text
        else:
            self.texts = [text]

        self.texts = [str(text) for text in self.texts]
        self.character = character
        self.tag = tag
        self.char_delay = char_delay
        self.line_delay = line_delay
        self.line_symbol = line_symbol
        self.newline = newline

    @staticmethod
    def from_dict(data) -> 'DisplayText':
        text = data.get("text", None)
        character = data.get("character", None)
        if text is None:
            raise ValueError("An error occured while initializing DisplayText: no text provided")
        tag = data.get("tag", None)
        char_delay = data.get("char_delay", None)
        line_delay = data.get("line_delay", None)
        return DisplayText(text=text, character=character, tag=tag, char_delay=char_delay, line_delay=line_delay)

    def add_text(self, text: str|list[str]) -> None:
        if isinstance(text, list):
            self.texts.extend(text)
        else:
            self.texts.append(text)
    
    def get_texts(self) -> list[dict]:
        result = []
        for text in self.texts:
            if self.character:
                result.append({"text": self.character.upper(), "tag": self.character, "char_delay": 0, "line_delay": 0, "newline": False})
            if self.line_symbol and self.character:
                result.append({"text": " "*self.CHARACTER_SPACES[self.character]+"> ", "tag": "computer", "char_delay": 0, "line_delay": 0, "newline": False})
            elif self.line_symbol:
                result.append({"text": "> ", "tag": "computer", "char_delay": 0, "line_delay": 0, "newline": False})
            result.append({"text": text, "tag": self.tag, "char_delay": self.char_delay, "line_delay": self.line_delay, "newline": self.newline})
        return result