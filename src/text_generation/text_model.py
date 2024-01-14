import random
from src.text_generation.template import Template
from src.utils.file_operations import construct_path, files_in_directory, file_to_dict

MODEL_CATEGORIES = ["planet_report", "topography"]
TEXT_MODEL_FILE_PATH = construct_path("src/data/text_models/{category}/")

class TextModel():
    def __init__(self, name: str, replace_values: dict[str, list[str]], templates: list[Template]) -> None:
        self.name = name
        self.replace_values = replace_values
        self.templates = templates

        self.required_data = self.get_required_data()

    @staticmethod
    def from_dict(data: dict) -> 'TextModel':
        name = data.get("name", None)
        templates_data = data.get("templates", None)
        replace_values = data.get("replace_values", None)

        if not isinstance(templates_data, list):
            raise ValueError(f"Invalid template data for text model {name}")
        if not isinstance(replace_values, dict):
            raise ValueError(f"Invalid replace values for text model {name}")
        
        templates = []
        for template_data in templates_data:
            try:
                template = Template.from_dict(data=template_data)
                templates.append(template)
            except ValueError as e:
                raise ValueError(f"An error occured while initializing text model {name}: {e}")
            
        text_model = TextModel(
            name=name,
            replace_values=replace_values,
            templates=templates
        )

        return text_model
    
    def get_required_data(self) -> set[str]:
        available_keys = set(self.replace_values.keys())
        required_data = set()
        for template in self.templates:
            placeholders = template.get_placeholders() - available_keys
            required_data.update(placeholders)
        return required_data
    
    def validate_given_data(self, data: dict) -> None:
        missing_keys = self.required_data - set(data.keys())
        if missing_keys:
            raise ValueError(f"Missing placeholder keys: {missing_keys}")
        for key, value in data.items():
            if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                raise ValueError(f"Invalid data for placeholder key {key}")

    def generate(self, **kwargs) -> str:
        self.validate_given_data(kwargs)
        kwargs.update(self.replace_values)
        
        template = random.choice(self.templates)
        text = template.generate(**kwargs)
        return text

class TextModelLibrary():
    _instance = None

    def __init__(self) -> None:
        if TextModelLibrary._instance is not None:
            raise RuntimeError("Tried to initialize multiple instances of TextModelLibrary.")
        self.text_models: dict[str, TextModel] = {}
        
        for category in MODEL_CATEGORIES:
            self._load_model_category(category=category)

    def _load_model_category(self, category: str) -> None:
        path = TEXT_MODEL_FILE_PATH.format(category=category)
        for file in files_in_directory(path=path, suffix='.json'):
            name = file[:-5]
            self.text_models[name] = self._load_model_from_file(file_path=path+file, model_name=name)

    @staticmethod
    def _load_model_from_file(file_path: str, model_name: str) -> TextModel:
        try:
            model_data = file_to_dict(file_path=file_path)
        except FileNotFoundError:
            raise ValueError(f"Text model {model_name} does not exist")
        
        model_data["name"] = model_name
        
        try:
            model = TextModel.from_dict(data=model_data)
        except ValueError as e:
            raise ValueError(f"An error occured while initializing text model {model_name} from path {file_path}: {e}")
        
        return model

    @staticmethod
    def get_instance() -> 'TextModelLibrary':
        if TextModelLibrary._instance is None:
            TextModelLibrary._instance = TextModelLibrary()
        return TextModelLibrary._instance
    
    def get_model(self, model_name: str) -> TextModel:
        if model_name not in self.text_models:
            raise ValueError(f"Text model '{model_name} does not exist")
        return self.text_models[model_name]