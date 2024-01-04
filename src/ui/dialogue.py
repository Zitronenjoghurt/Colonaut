from copy import deepcopy
from src.ui.display_text import DisplayText
from src.constants.custom_exceptions import EventTypeNotSubscribedError
from src.modules.utilities import construct_path, file_to_dict, files_in_directory
from src.events.event import Event
from src.events.event_bus import EventBus

EVENT_BUS = EventBus.get_instance()
DIALOGUE_CATEGORIES = ["system"]
DIALOGUE_FILE_PATH = construct_path("src/data/dialogue/{dialogue_category}/")

class Dialogue():
    def __init__(self, name: str, display_texts: list[DisplayText]) -> None:
        self.name = name
        self.display_texts = display_texts
        self.current_index = 0
        self.action_pending = False
        self.actions = {}
        self.event_pending = False
        self.event = None
        self.id_index_map = {}

        # Register indices for entry ids
        for i, display_text in enumerate(self.display_texts):
            id = display_text.get_id()
            if id in self.id_index_map:
                raise RuntimeError(f"An error occured while loading dialogue '{name}': the id '{id}' of entry at index {i} already exists at index {self.id_index_map[id]}.")
            if id != "":
                self.id_index_map[id] = i
        
        # Verify action target ids
        for i, display_text in enumerate(self.display_texts):
            actions = display_text.get_actions()
            if len(actions) == 0:
                continue
            for action_target in actions.values():
                if action_target not in self.id_index_map:
                    raise RuntimeError(f"An error occured while loading dialogue '{name}': the action of the entry at index {i} references an invalid id '{action_target}'.")
            
    
    def get_texts(self) -> list[DisplayText]:
        display_texts = []

        i: int = self.current_index
        while i < len(self.display_texts): 
            self.current_index = i
            display_text = self.display_texts[i]
            display_texts.append(display_text)

            event_type = display_text.get_event()
            if isinstance(event_type, str):
                event_data = display_text.get_event_data()
                try:
                    if isinstance(event_data, dict):
                        self.event = Event(type=event_type, **event_data)
                        self.event_pending = True
                    else:
                        self.event = Event(type=event_type)
                        self.event_pending = True
                except EventTypeNotSubscribedError:
                    raise RuntimeError(f"An error occured while playing dialogue {self.name} at index {i}: Event {event_type} does not exist or was not subscribed on.")

            if display_text.is_jumping():
                jump_id = display_text.get_jump_to()
                jump_index = self.id_index_map.get(jump_id, None)
                if jump_index is None:
                    raise RuntimeError(f"An error occured while playing dialogue {self.name} at index {i}: tried to jump to id {jump_id}, but no entry with this id was found.")
                i = jump_index
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
    
    def has_pending_event(self) -> bool:
        return self.event_pending
    
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
        next_id = self.actions[action_name]
        next_index = self.id_index_map.get(next_id, None)
        if next_index is None:
            raise RuntimeError(f"An error occured while playing dialogue {self.name}: tried to process action {action_name}, but no entry with the target id {next_id} was found.")
        self.current_index = next_index
        self.action_pending = False
        self.actions = {}

    def process_event(self) -> None:
        if not self.event_pending or not isinstance(self.event, Event):
            raise RuntimeError(f"An error occured while playing dialogue {self.name}: tried to process event, but no event is pending.")
        response = EVENT_BUS.publish(self.event)
        self.event_pending = False
        self.event = None
    
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
        return Dialogue(name=dialogue_name, display_texts=display_texts)
    
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