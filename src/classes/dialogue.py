from src.modules.utilities import construct_path, file_to_dict
from .display_text import DisplayText

DIALOGUE_FILE_PATH = construct_path("src/data/dialogue/{dialogue_name}.json")

class Dialogue():
    LIBRARY = {}

    def __init__(self, display_texts: list[DisplayText]) -> None:
        self.display_texts = display_texts
    
    @staticmethod
    def load(dialogue_name: str) -> 'Dialogue':
        dialogue_name = dialogue_name.lower()
        dialogue = Dialogue.LIBRARY.get(dialogue_name, None)
        if dialogue is None:
            dialogue = Dialogue._load_from_file(dialogue_name=dialogue_name)
            Dialogue.LIBRARY[dialogue_name] = dialogue
        return dialogue

    @staticmethod
    def _load_from_file(dialogue_name: str) -> 'Dialogue':
        try:
            path = DIALOGUE_FILE_PATH.format(dialogue_name=dialogue_name)
            dialogue = file_to_dict(file_path=path)
        except FileNotFoundError:
            raise ValueError(f"Dialogue {dialogue_name} does not exist.")
        
        dialogue_text = dialogue.get("text", None)
        if dialogue_text is None:
            raise ValueError(f"Dialogue {dialogue_name} does not include any text.")
        
        display_texts = []
        for display_text in dialogue_text:
            try:
                display_texts.append(DisplayText.from_dict(display_text))
            except ValueError as e:
                raise ValueError(f"An error occured while trying to initialize Dialogue {dialogue_name}: {e}")
        return Dialogue(display_texts=display_texts)
    
    def get_texts(self) -> list[DisplayText]:
        return self.display_texts