from typing import Any, Optional
from .config import Config

CONFIG = Config.get_instance()

class DisplayText:
    CHARACTER_SPACES = {
        "energy": 0,
        "lifesupport": 0,
        "nexus": 0,
        "sensor": 0,
        "you": 0
    }

    def __init__(
            self, 
            text: str|list[str], 
            actions: Optional[dict] = None, 
            action_answers: Optional[dict] = None, 
            character: Optional[str] = None, 
            tag: Optional[str] = None, 
            char_delay: Optional[int] = None, 
            line_delay: Optional[int] = None, 
            line_symbol: Optional[bool] = None, 
            newline: Optional[bool] = None,
            id: Optional[str] = None,
            jump_to: Optional[str] = None, 
            event: Optional[str] = None,
            event_data: Any = None
        ) -> None:
        if actions is None:
            actions = {}
        if action_answers is None:
            action_answers = {}
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
        self.actions = actions
        self.action_answers = action_answers
        self.character = character
        self.tag = tag
        self.char_delay = char_delay
        self.line_delay = line_delay
        self.line_symbol = line_symbol
        self.newline = newline
        self.id = id
        self.jump_to = jump_to
        self.event = event
        self.event_data = event_data

    @staticmethod
    def from_dict(data) -> 'DisplayText':
        text = data.get("text", None)
        if text is None:
            raise ValueError("An error occured while initializing DisplayText: no text provided")
        actions = data.get("actions", None)
        action_answers = data.get("action_answers", None)
        character = data.get("character", None)
        tag = data.get("tag", None)
        char_delay = data.get("char_delay", None)
        line_delay = data.get("line_delay", None)
        newline = data.get("newline", None)
        line_symbol = data.get("line_symbol", None)
        id = data.get("id", None)
        jump_to = data.get("jump_to", None)
        event = data.get("event", None)
        event_data = data.get("event_data", None)
        return DisplayText(
            text=text, 
            actions=actions, 
            action_answers=action_answers, 
            character=character, 
            tag=tag, 
            char_delay=char_delay, 
            line_delay=line_delay, 
            newline=newline, line_symbol=line_symbol,
            id=id,
            jump_to=jump_to,
            event=event,
            event_data=event_data
        )

    def add_text(self, text: str|list[str]) -> None:
        if isinstance(text, list):
            self.texts.extend(text)
        else:
            self.texts.append(text)
    
    def get_texts(self) -> list[dict]:
        result = []
        for i, text in enumerate(self.texts):
            if self.line_symbol and self.character:
                result.append({"text": self.character.upper(), "tag": self.character, "char_delay": 0, "line_delay": 0, "newline": False})
                result.append({"text": " "*self.CHARACTER_SPACES[self.character]+"> ", "tag": "computer", "char_delay": 0, "line_delay": 0, "newline": False})
            elif self.line_symbol:
                result.append({"text": "> ", "tag": "computer", "char_delay": 0, "line_delay": 0, "newline": False})
            if i+1 == len(self.texts) and self.has_actions():
                result.append({"text": text, "tag": self.tag, "char_delay": self.char_delay, "line_delay": 0, "newline": self.newline})
            else:
                result.append({"text": text, "tag": self.tag, "char_delay": self.char_delay, "line_delay": self.line_delay, "newline": self.newline})
        return result
    
    def get_actions(self) -> dict:
        return self.actions
    
    def get_action_answer(self, action_name: str) -> 'DisplayText':
        if action_name not in self.action_answers:
            answer = action_name
        else:
            answer = self.action_answers[action_name]
        return DisplayText(text=answer, character="you", char_delay=0, line_delay=self.line_delay)
    
    def has_actions(self) -> bool:
        return len(self.actions) > 0
    
    def get_id(self) -> str:
        if self.id:
            return self.id
        else:
            return ""
    
    def is_jumping(self) -> bool:
        return isinstance(self.jump_to, str)
    
    def get_jump_to(self) -> str:
        if self.jump_to:
            return self.jump_to
        else:
            return ""
        
    def get_event(self) -> Optional[str]:
        return self.event
    
    def get_event_data(self) -> Any:
        return self.event_data