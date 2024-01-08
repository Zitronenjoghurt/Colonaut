from datetime import datetime
from typing import Any, Optional
from src.constants.response_types import ResponseTypes

class Response():
    TYPES = ResponseTypes

    def __init__(self, data: Any = None, typed: bool = False) -> None:
        self.data: Any = data
        self.typed = typed
        self.timestamp = datetime.now()

    # Response is true if its not empty
    def __bool__(self):
        if self.data is None:
            return False
        return len(self.data) != 0
    
    def get_data(self, response_type: Optional[str] = None) -> Any:
        if not self.typed or not response_type:
            return self.data
        return self.data.get(response_type, None)
    
    def has_type(self, response_type: str) -> bool:
        return response_type in self.data

    def validate_data(self, validation_type: type) -> bool:
        return isinstance(self.data, validation_type)
    
    @staticmethod
    def create(data: Any = None, response_type: Optional[str] = None) -> 'Response':
        response_data = data
        typed = False
        if response_type is not None:
            response_data = {
                response_type: data
            }
            typed = True
        return Response(data=response_data, typed=typed)
    
    def fuse(self, other: 'Response') -> 'Response':
        if not isinstance(other, Response):
            raise ValueError("An error occured while trying to fuse two responses: given response is not of class Response")
        if not self.typed and not self:
            return other # self has no data, return other
        if not other.typed and not other:
            return self # other  has no data, return self
        if not self.typed or not other.typed:
            raise ValueError("An error occured while trying to fuse two responses: you can only fuse 2 typed responses or a response with an empty response")
        # Since its typed, data will always be a dict
        data = self.data
        data.update(other.data)
        return Response(data=data, typed=True)
    
    def add_data(self, data: Any, response_type: str) -> None:
        self.data[response_type] = data