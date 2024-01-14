import random
import re

class Template():
    def __init__(self, text: str) -> None:
        self.text = text

        pattern = r"\{(\w+)\}"
        self.placeholders = set(re.findall(pattern, self.text))
    
    @staticmethod
    def from_dict(data: dict) -> 'Template':
        retrieved_data = {
            "text": data.get("text", None)
        }

        for key, value in retrieved_data.items():
            if value is None:
                raise ValueError(f"An error occured while initializing text template: missing data '{key}")
            
        template = Template(
            text=retrieved_data["text"]
        )

        return template
    
    def get_placeholders(self) -> set[str]:
        return self.placeholders
    
    def get_values_from_data(self, data: dict) -> dict[str, str]:
        values = {}
        for placeholder in self.placeholders:
            value = data.get(placeholder, None)
            if value is None or not isinstance(value, list):
                raise RuntimeError(f"An unexpected error occured while retrieving replace values for template generation from given data {data}")
            values[placeholder] = random.choice(value)
        return values
    
    def generate(self, **kwargs) -> str:
        replace_values = self.get_values_from_data(kwargs)
        result = self.text.format(**replace_values)
        return result