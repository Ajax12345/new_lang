import lang_exceptions, typing
import lang_utility_objs

class NameObj:
    def __init__(self, _token) -> None:
        self.token = _token
    @property
    def ast_type(self):
        return 'name'
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.token})'
    def __getattr__(self, _attr:str) -> typing.Any:
        return getattr(self.token, _attr)

class OperatorObj:
    def __init__(self, _token) -> None:
        self.token = _token
    @property
    def ast_type(self):
        return 'operator'
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.token})'
    def __getattr__(self, _attr:str) -> typing.Any:
        return getattr(self.token, _attr)

class AttrLookup:
    def __init__(self, _path:typing.List[str]) -> None:
        self.path = _path
    @property
    def ast_type(self):
        return 'attr_lookup'
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.token})'

class Signature:
    def __init__(self, _signature:list) -> None:
        self.signature = _signature
    @property
    def ast_type(self):
        return 'signature'
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.signature})'

class NameLookup:
    def __init__(self, _lookup:list) -> None:
        self.lookup = _lookup
    @property
    def ast_type(self):
        return 'name_lookup'
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.lookup})'

class LParen:
    @property
    def ast_type(self):
        return 'lparen'
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("(")'
        
class RParen:
    @property
    def ast_type(self):
        return 'rparen'
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(")")'

class TypeObj:
    def __init__(self, _token) -> None:
        self.token = _token
    @property 
    def ast_type(self):
        return 'type_obj'
    def __getattr__(self, _attr:str) -> None:
        return getattr(self.token, _attr)
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.token})'

class TrailingNameLookup(NameLookup):
    @property 
    def ast_type(self):
        return 'trailing_name_lookup'


class FullAst:
    from_loop = None
    @classmethod
    def generate_ast(cls, _stream:typing.Iterator, _ast = None) -> typing.Any:
        if _ast is None:
            _ast = lang_utility_objs.RunningNames(cls.from_loop)
            '''
            if not _ast:
                raise lang_exceptions.InvalidSyntax(f"In '{cls.from_loop.file}', line {cls.from_loop.line_counter.line_number}:\nInvalid Syntax: ")
            '''
        _start = next(_stream, None)
        if _start is None:
            return _ast
        if _start in _ast:
            while _start and _start in _ast:
                _ast.push(_start)
                _start = next(_stream, None)
            _stream = iter([_start, *_stream])
            return cls.generate_ast(_stream, _ast = _ast)
        if _start.name in {'mul', 'div'}: 
            new_ast = lang_utility_objs.RunningNames(cls.from_loop)
            _new_check = next(_stream, None)
            while _new_check and _new_check in new_ast:
                new_ast.push(_new_check)
                _new_check = next(_stream, None)
            _stream = iter([_new_check, *_stream])
            return cls.generate_ast(_stream, lang_utility_objs.Operation(_ast, _start, new_ast))
        return lang_utility_objs.Operation(_ast, _start, cls.generate_ast(_stream, _ast = None))
            

def generate_ast(_execute=False) -> typing.Callable:  
    def _generate(_f:typing.Callable) -> typing.Callable:
        def _wrapper(cls, from_loop, *args, **kwargs) -> typing.Any:
            result, delim, end = _f(cls, from_loop, *args, **kwargs)
            if not _execute:
                return result, delim, end
            FullAst.from_loop = from_loop
            return FullAst.generate_ast(iter(result)), delim, end
        return _wrapper
    return _generate


class AST:
    def __init__(self, _from_loop, _delimeter:lang_utility_objs.ast_delimeters) -> None:
        self.__dict__ = _from_loop.__dict__
        self.delimeter, self.from_source =_delimeter, _from_loop
    def attr_lookup(self, _c):
        while _c and _c.name == 'dot':
            _attr = next(self.header, None)
            if _attr is None:
                raise lang_exceptions.InvalidSyntax(f"In '{self.file}', line {self.line_counter.line_number}:\nInvalid Syntax: unexpected termination of expression")
            if _attr.name != 'variable':
                raise lang_exceptions.InvalidSyntax(f"In '{self.file}', line {self.line_counter.line_number}:\nInvalid Syntax: '{_attr.value}'")
            yield _attr
            _c = next(self.header, None)
            if _c is None:
                break
            
        if _c is not None:
            self.header = iter([_c, *self.header])

    def start(self) -> None:
        _start, _queue = next(self.header, None), []
        while _start is not None and _start.name not in self.delimeter:
            if _start.token_type in {'name', 'boolean', 'value', 'lang_type'}:
                _queue.append(NameLookup([_start, *self.attr_lookup(next(self.header, None))]))
            elif _start.token_type in {'operator'}:
                _queue.append(OperatorObj(_start))
            elif _start.name == 'lparen':
                _signature = []
                while True:
                    _param, end, _ending_token = self.__class__.create_ast(self.from_source, lang_utility_objs.ast_delimeters('comma', 'rparen'))
                    if _param:
                        _signature.append(_param)
                    if _ending_token is None or _ending_token.name == 'rparen':
                        break
                _queue.append(Signature(_signature))
            elif _start.name == 'dot':
                _lookup = list(self.attr_lookup(_start))
                if not _lookup:
                    raise lang_exceptions.InvalidSyntax(f"In '{self.file}', line {self.line_counter.line_number}:\nInvalid Syntax: '{_start.value}'")
                _queue.append(TrailingNameLookup(_lookup))
            _start = next(self.header, None)
        return _queue, self.delimeter, _start      

    @classmethod
    @generate_ast(True)
    def create_ast(cls, _from_loop, _delimeter:lang_utility_objs.ast_delimeters) -> typing.Any:
        _ast = cls(_from_loop, _delimeter)
        return _ast.start()

    
  
