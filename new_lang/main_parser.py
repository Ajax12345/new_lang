import typing, lang_wrappers
import collections.abc, lang_exceptions
import parser_identifiers



class Scope:
    def __init__(self, scope:str='__main__', is_main:bool=True) -> None:
        self.scope, self.is_main = scope, is_main

class parser_Header:
    def __init__(self, *args) -> None:
        self.start_token, self.parser_obj, self.header, self.lines, self.line_counter, self.file, self.current_level, self.scope = args

class LineCount:
    def __init__(self, _start:int = 1) -> None:
        self._starting = _start
    @property
    def line_number(self):
        return self._starting
    def __next__(self):
        self._starting += 1

class _func(parser_Header):
    def signature(self) -> None:
        pass
    def abstract(self) -> None:
        pass

    def start(self) -> None:
        _name = next(self.header, None)
        if _name is None or _name.token_type != 'name':
            raise lang_exceptions.InvalidFunctionName(f"In '{self.file}', line {self.line_counter.line_number}:\nInvalid Function Name: expected a name")
        _next = next(self.header, None)
        if _next is None:
            raise lang_exceptions.InvalidFunctionName(f"In '{self.file}', line {self.line_counter.line_number}:\nInvalid Function Name: expecting a signature or utility")
        if _next.name == 'dot':
            _utility_name = next(self.header, None)
           
            if _utility_name is None:
                raise lang_exceptions.InvalidFunctionName(f"In '{self.file}', line {self.line_counter.line_number}:\nInvalid Function Name: expecting utility name")
            getattr(self, _utility_name.value)()
        elif _next.name == 'lparent':
            pass
        else:
            lang_exceptions.InvalidFunctionName(f"In '{self.file}', line {self.line_counter.line_number}:\nInvalid Function Name: expecting a signature or utility")
    @classmethod
    def init_identifier(cls, parser_obj, _header:typing.Iterator, _lines:typing.Iterator, _line_counter:LineCount, _file:str, _current_level:int, scope:Scope) -> typing.Any:
        _func_inst = cls(None, parser_obj, _header, _lines, _line_counter, _file, _current_level, scope)
        _func_inst.start()
        return 

class ParseDenote:
    idenifiers = {'func':_func}
    @classmethod
    def get_obj_ast(cls, _, _parser_obj, _header:typing.Iterator, _lines:typing.Iterator, _line_counter:LineCount, _file:str, _current_level:int, scope:Scope) -> typing.Any:
        _identifier = next(_header, None)
        if _identifier is None:
            raise lang_exceptions.InvalidSyntax(f"In '{_file}', line {_line_counter.line_number}:\nInvalid Syntax Error: expected identifier name")
        if _identifier.value not in cls.idenifiers:
            raise lang_exceptions.InvalidIdentifier(f"In '{_file}', line {_line_counter.line_number}:\nInvalid Indentifier: '{_identifier.value}'")
        _ = cls.idenifiers[_identifier.value].init_identifier(_parser_obj, _header, _lines, _line_counter, _file, _current_level+4, scope)        


class _AST_op(parser_Header):
    def start(self) -> None:
        _identifier = next(self.header, None)
        print(_identifier)
        if _identifier.name not in {'colon', 'dot', 'lparent', 'assign'}:
            raise lang_exceptions.InvalidSyntax(f"In '{_file}', line {_line_counter.line_number}:\nInvalid Syntax: invalid syntax with name '{_identifier.value}'")

    @classmethod
    def get_obj_ast(cls, _start_token, _parser_obj, _header:typing.Iterator, _lines:typing.Iterator, _line_counter:LineCount, _file:str, _current_level:int, scope:Scope) -> typing.Any:
        #_ = cls.idenifiers[_identifier.value].init_identifier(_parser_obj, _header, _lines, _line_counter, _file, _current_level, scope)        
        _main_execute = cls(_start_token, _parser_obj, _header, _lines, _line_counter, _file, _current_level, scope)
        _main_execute.start()
        return 

class Parser:
    def __init__(self, _file:str, scope:Scope, _whitespace:int = 0, _line_count = 1) -> None:
        self.file, self.level, self.line_count = _file, _whitespace, LineCount(_line_count)
        self.scope = scope
        self.token_matcher = {'at':ParseDenote, 'name':_AST_op}
    @property
    def stream(self) -> typing.Iterator:
        return self._stream
    @stream.setter
    def stream(self, _full_stream) -> None:
        self._stream = _full_stream
    def __next__(self):
        return next(self.stream, None)

    def start(self) -> None:
        _start = next(self, None)
        while _start is not None:
            _t, *_trailing = _start
            if self.level and not _t.is_space or _t.is_space and self.level != len(_t):
                raise lang_exceptions.IndentationError(f"In '{self.file}', line {self.line_count.line_number}:\nIndentationError: expected {self.level}, got {len(_t)}")
            _trailing = iter(_trailing)
            if _t.is_space:
                _t, *_trailing = _trailing
                _trailing = iter(_trailing)
            if _t.token_type not in self.token_matcher:
               raise lang_exceptions.InvalidSyntax(f"In '{self.file}', line {self.line_count.line_number}:\nInvalid Syntax: invalid identifier '{_t.value}'") 
            _ = self.token_matcher[_t.token_type].get_obj_ast(_t, self.__class__, _trailing, self.stream, self.line_count, self.file, self.level, self.scope)

            _start = next(self, None)
            next(self.line_count)

    @classmethod
    def load_tokens(cls, _file:str, _tokens:typing.Iterator, _indent:int=0, _line:int=1, _start:bool = True, scope='__main__') -> None:
        if not isinstance(_tokens, collections.abc.Iterator):
            raise TypeError(f"'load_tokens' requires an iterator, got {type(_tokens).__name__}")
        _parser = cls(_file, Scope(scope=scope, is_main = scope == '__main__'), _whitespace = _indent, _line_count = _line)
        _parser.stream = _tokens
        if _start:
            _parser.start()
