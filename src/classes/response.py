from datetime import datetime
from typing import Any
from ..constants.response_types import ResponseTypes

class Response():
    TYPES = ResponseTypes

    def __init__(self, message: str = "", data = None, response_type: str = "") -> None:
        self.message = message
        self.data = data
        self.type = response_type.lower()
        self.timestamp = datetime.now()

    # Response is true if its not empty
    def __bool__(self):
        return len(self.message) > 0 and self.data is not None
    
    def get_message(self) -> str:
        return self.message
    
    def get_data(self) -> Any:
        return self.data
    
    def get_type(self) -> str:
        return self.type

    def of_type(self, response_type: str) -> bool:
        return self.type == response_type.lower()

    def validate_data(self, validation_type: type) -> bool:
        return isinstance(self.data, validation_type)
    
    @staticmethod
    def create(message: str = "", data: Any = None, response_type: str = "") -> 'Response':
        return Response(message=message, data=data, response_type=response_type)
    
    @staticmethod
    def from_data(data: Any, response_type: str = "") -> 'Response':
        return Response(data=data, response_type=response_type)
    
    @staticmethod
    def from_message(message: str, response_type: str = "") -> 'Response':
        return Response(message=message, response_type=response_type)