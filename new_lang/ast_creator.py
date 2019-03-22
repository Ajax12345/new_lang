import lang_exceptions, typing


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

class AST:
    def __init__(self, _from_loop, _delimeter = None) -> None:
        self.__dict__ = {**_from_loop.__dict__, 'delimeter':_delimeter, 'from_source':_from_loop}
    def attr_lookup(self, _c):
        while _c.name == 'dot':
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
        while _start is not None and (True if self.delimeter is None else _start.name not in self.delimeter):
            if _start.token_type in {'name', 'boolean', 'value'}:
                _new_queue = [_start]
                _check_next = next(self.header, None)
                if _check_next is None:
                    _queue.append(NameLookup(_new_queue))
                    break
                if _check_next.token_type in {'operator'}:
                    _queue.append(NameLookup(_new_queue))
                    _queue.append(OperatorObj(_check_next))
                elif _check_next.name in {'dot', 'lparen'}:
                    if _check_next.name == 'dot':
                        _new_queue.extend(list(self.attr_lookup(_check_next)))
                        _queue.append(NameLookup(_new_queue))
                        #self.header = iter([_second_check_next, *self.header])
                            
                    else:
                        _signature = []
                        while True:
                            _param, end, _ending_token = self.__class__.create_ast(self.from_source, _delimeter={'comma', 'rparen'})
                            print('testing here sig', _param, end, _ending_token)
                            if _param:
                                _signature.append(_param)
                            if _ending_token is None or _ending_token.name == 'rparen':
                                break
                        _queue.append(NameLookup(_new_queue))
                        _queue.append(Signature(_signature))
                    _check_next = next(self.header, None)
                    if _check_next is None:
                        break
                
                    self.header = iter([_check_next, *self.header])
                elif _check_next.name == 'rparen':
                    _queue.append(NameLookup(_new_queue))
                    if self.delimeter and _check_next.name in self.delimeter:
                        return _queue, self.delimeter, _check_next
                    _queue.append(RParen())
                   
                elif _check_next.name in self.delimeter:
                    _queue.append(NameLookup(_new_queue))
                    return _queue, self.delimeter, _check_next
                else:
                    raise lang_exceptions.InvalidSyntax(f"In '{self.file}', line {self.line_counter.line_number}:\nInvalid Syntax: '{_check_next.value}'")

            elif _start.token_type in {'operator'}:
                
                _queue.append(OperatorObj(_start))
            elif _start.name == 'lparen':
                _queue.append(LParen())
            elif _start.name == 'rparen':
                _queue.append(RParen())
            else:
                raise lang_exceptions.InvalidSyntax(f"In '{self.file}', line {self.line_counter.line_number}:\nInvalid Syntax: '{_start.value}'")
            _start = next(self.header, None)
        return _queue, self.delimeter, _start      

    @classmethod
    def create_ast(cls, _from_loop, _delimeter = None) -> typing.Any:
        _ast = cls(_from_loop, _delimeter = _delimeter)
        return _ast.start()
  
