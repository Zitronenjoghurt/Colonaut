from copy import deepcopy
from src.modules.utilities import construct_path, file_to_dict, files_in_directory
from .display_text import DisplayText

DIALOGUE_CATEGORIES = ["system"]
DIALOGUE_FILE_PATH = construct_path("src/data/dialogue/{dialogue_category}/")

class Dialogue():
    def __init__(self, display_texts: list[DisplayText]) -> None:
        self.display_texts = display_texts
        self.current_index = 0
        self.action_pending = False
        self.actions = {}
    
    def get_texts(self) -> list[DisplayText]:
        display_texts = []

        i: int = self.current_index
        while i < len(self.display_texts): 
            self.current_index = i
            display_text = self.display_texts[i]
            display_texts.append(display_text)

            if display_text.is_jumping():
                i = display_text.get_jump_to()
                continue

            if display_text.has_actions():
                self.action_pending = True
                self.actions = display_text.get_actions()
                break

            i = i + 1
        return display_texts
    
    def reset(self) -> None:
        self.current_index = 0
    
    def waiting_for_action(self) -> bool:
        return self.action_pending
    
    def is_finished(self) -> bool:
        return self.current_index + 1 == len(self.display_texts)
    
    def get_action_labels(self) -> list[str]:
        return list(self.actions.keys())
    
    def get_action_answer(self, action_name: str) -> DisplayText:
        if action_name not in self.actions:
            raise RuntimeError(f"Action {action_name} does not exist in the current dialogue.")
        return self.display_texts[self.current_index].get_action_answer(action_name=action_name)
    
    def process_action(self, action_name: str) -> None:
        if action_name not in self.actions:
            raise RuntimeError(f"Action {action_name} does not exist in the current dialogue.")
        self.current_index = self.actions[action_name]
        self.action_pending = False
        self.actions = {}
    
class DialogueLibrary():
    _instance = None

    def __init__(self) -> None:
        if DialogueLibrary._instance is not None:
            raise RuntimeError("Tried to initialize multiple instances of DialogueLibrary.")
        self.dialogue_by_category = {}
        self.category_by_dialogue = {}
        for category in DIALOGUE_CATEGORIES:
            category_dialogues = self._load_dialogue_category(category=category)
            self.dialogue_by_category[category] = category_dialogues
            for dialogue_name in category_dialogues.keys():
                self.category_by_dialogue[dialogue_name] = category

    def _load_dialogue_category(self, category: str) -> dict[str, Dialogue]:
        dialogues = {}
        category_file_path = DIALOGUE_FILE_PATH.format(dialogue_category=category)
        for file in files_in_directory(category_file_path, 'json'):
            dialogue_name = file[:-5]
            dialogues[dialogue_name] = self._load_dialogue_from_file(category_file_path + file, dialogue_name)
        return dialogues
    
    @staticmethod
    def _load_dialogue_from_file(file_path: str, dialogue_name: str) -> 'Dialogue':
        try:
            dialogue = file_to_dict(file_path=file_path)
        except FileNotFoundError:
            raise ValueError(f"Dialogue {dialogue_name} does not exist.")

        dialogue_text = dialogue.get("text", None)
        if dialogue_text is None:
            raise ValueError(f"Dialogue {dialogue_name} does not include any text.")
        
        options = dialogue.get("options", {})
        display_texts = []
        for display_text in dialogue_text:
            DialogueLibrary._set_default_text_options(options=options, display_text=display_text)
            try:
                display_texts.append(DisplayText.from_dict(display_text))
            except ValueError as e:
                raise ValueError(f"An error occured while trying to initialize Dialogue {dialogue_name}: {e}")
        return Dialogue(display_texts=display_texts)
    
    @staticmethod
    def _set_default_text_options(options: dict, display_text: dict) -> None:
        if len(options) == 0:
            return
        
        default_options = {
            "actions": options.get("actions", None),
            "character": options.get("character", None),
            "tag": options.get("tag", None),
            "char_delay": options.get("char_delay", None),
            "line_delay": options.get("line_delay", None),
            "line_symbol": options.get("line_symbol", None),
            "newline": options.get("newline", None)
        }

        for option, value in default_options.items():
            if value is not None and option not in display_text:
                display_text[option] = value

    @staticmethod
    def get_instance() -> 'DialogueLibrary':
        if DialogueLibrary._instance is None:
            DialogueLibrary._instance = DialogueLibrary()
        return DialogueLibrary._instance
    
    def get_dialogue_by_name(self, dialogue_name: str) -> 'Dialogue':
        try:
            category = self.get_dialogue_category(dialogue_name=dialogue_name)
        except ValueError as e:
            raise ValueError(f"An error occured while retrieving dialogue {dialogue_name}: {e}")
        return deepcopy(self.dialogue_by_category[category][dialogue_name])

    def get_dialogue_category(self, dialogue_name: str) -> str:
        if dialogue_name not in self.category_by_dialogue:
            raise ValueError(f"Dialogue {dialogue_name} does not exist.")
        return self.category_by_dialogue[dialogue_name]