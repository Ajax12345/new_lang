import typing, lang_wrappers

class Parser:
    def __init__(self, _whitespace:int = 0) -> None:
        self.level = _whitespace
    @property
    def stream(self) -> typing.Iterator:
        return self._stream
    @stream.setter
    @lang_wrappers.is_iterator
    def stream(self, _full_stream) -> None:
        return self._stream = _full_stream
    @classmethod
    @lang_wrappers.is_iterator
    def load_tokens(cls, _tokens:typing.Iterator) -> None:
        pass