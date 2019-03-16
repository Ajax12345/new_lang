import typing, lang_wrappers
import collections.abc, lang_exceptions
import itertools

class _line_count:
    def __init__(self, _start:int = 1) -> None:
        self._starting = _start
    @property
    def line_number(self):
        return self._starting
    def __next__(self):
        self._starting += 1

class Parser:
    def __init__(self, _file, _whitespace:int = 0, _line_count = 1) -> None:
        self.file, self.level, self.line_count = _file, _whitespace, _line_count(_line_count)

    @property
    def stream(self) -> typing.Iterator:
        return self._stream
    @stream.setter
    @lang_wrappers.is_iterator
    def stream(self, _full_stream) -> None:
        return self._stream = _full_stream
    def __next__(self):
        return next(self.stream, None)

    def start(self) -> None:
        _start = next(self)
        while _start is not None:
            _t, *_trailing = _start
            if self.level and not _t.is_space or _t.is_space and self.level != len(_t):
                raise lang_exceptions.IndentationError(f"In '{self.file}', line {self.line_count.line_number}:\nIndentationError: expected {self.level}, got {len(_t)}")
            _start = next(self)
            next(self.line_count)

    @classmethod
    def load_tokens(cls, _file:str, _tokens:typing.Iterator, _indent:int=4, _line:int=1, _start:bool = True) -> None:
        if not isinstance(_tokens, collections.abc.Iterator):
            raise TypeError(f"'{_f.__name__}' requires an iterator, got {type(_iter).__name__}")
        _parser = cls(_file, _whitespace = _indent, _line_count = _line)
        _parser.stream = _tokens
        if _start:
            _parser.start()
