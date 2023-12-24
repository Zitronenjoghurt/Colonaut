from datetime import datetime
from typing import Any

class Response():
    def __init__(self, message: str = "", data = None) -> None:
        self.message = message
        self.data = data
        self.timestamp = datetime.now()

    # Response is true if its not empty
    def __bool__(self):
        return len(self.message) > 0 and self.data is not None
    
    def get_message(self) -> str:
        return self.message
    
    def get_data(self) -> Any:
        return self.data
    
    def validate_data(self, validation_type: type) -> bool:
        return isinstance(self.data, validation_type)
    
    @staticmethod
    def create(message: str = "", data: Any = None) -> 'Response':
        return Response(message=message, data=data)
    
    @staticmethod
    def from_data(data: Any) -> 'Response':
        return Response(data=data)
    
    @staticmethod
    def from_message(message: str) -> 'Response':
        return Response(message=message)