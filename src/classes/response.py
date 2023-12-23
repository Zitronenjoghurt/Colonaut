from typing import Any, Optional

class Response():
    def __init__(self, message: str = "", data = None) -> None:
        self.message = message
        self.data = data
    
    def get_message(self) -> str:
        return self.message
    
    def get_data(self) -> Any:
        return self.data
    
    @staticmethod
    def create(message: str = "", data: Any = None) -> 'Response':
        return Response(message=message, data=data)