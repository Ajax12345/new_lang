import typing

class _token:
    @property
    def is_space(self) -> bool:
        return self.token_type == 'whitespace'
    def __len__(self) -> int:
        return len(self.value)
    @property
    def is_denote(self) -> bool:
        return self.token_type == 'at'
    @property
    def is_identifier(self):
        return self.token_type == 'identifier'
    

    
class Token(_token):
    def __init__(self, _type:str, _name:str, _, _val:str) -> None:
        self.token_type, self.name, self.value = _type, _name, _val
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(type={self.token_type}, name={self.name}, value={self.value})'

    
