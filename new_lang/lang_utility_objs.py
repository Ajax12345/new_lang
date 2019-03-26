import typing
import lang_exceptions

class ast_delimeters:
    def __init__(self, *args:typing.List[str]) -> None:
        self.delims = args
    def __bool__(self):
        return bool(self.delims)
    def __contains__(self, _val:str) -> bool:
        return _val in self.delims
    def __repr__(self) -> str:
        return f"Delim({', '.join(self.delims)})"

class RunningNames:
    def __init__(self, from_loop_obj) -> None:
        self.names, self._valid = [], {'name_lookup', 'trailing_name_lookup', 'signature'}
        self.from_loop = from_loop_obj
    @property
    def name(self):
        return 'running_name'
    def __contains__(self, _namespace) -> bool:
        return _namespace.ast_type in self._valid
    def __bool__(self) -> bool:
        return bool(self.names)
    def __getattr__(self, _name):
        return getattr(self.from_loop, _name)
    def push(self, _name_action) -> None:
        if _name_action.ast_type == 'trailing_name_lookup' and (not self.names or (self.names and self.names[-1].ast_type != 'signature')):
            raise lang_exceptions.InvalidSyntax(f"In '{self.file}', line {self.line_counter.line_number}:\nInvalid Syntax: '.'")
        self.names.append(_name_action)
    def __repr__(self) -> str:
        return f'Namespace({self.names})'

class Operation:
    def __init__(self, _left, _op, _right) -> None:
        self.left, self.op, self.right = _left, _op, _right
    @property
    def name(self):
        return 'operation'
    def __bool__(self) -> bool:
        return True
    def __contains__(self, _) -> bool:
        return False
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.left}, {self.op.value}, {self.right})'

class NameAction:
    def __init__(self, _name_listing:list, _type, _action, _ast) -> None:
        self._name_listing, self.var_type, self.action, self.ast = _name_listing, _type, _action, _ast
    def __call__(self, _namespace:dict) -> typing.Any:
        """To run the ast"""
        pass
    def __repr__(self) -> str:
        return f"\n@name: {[i.value for i in self._name_listing]}\n@type: {self.var_type}\n@action: {self.action.value}\n@ast: {self.ast}"

class InPlaceAction:
    def __init__(self, _name_listing:list, _action) -> None:
        self.name_listing, self.action = _name_listing, _action
    def __call__(self, _namespace:dict) -> typing.Any:
        """To run the ast"""
        pass
    def __repr__(self) -> str:
        return f"\n@name: {[i.value for i in self.name_listing]}\n@action: {self.action.value}"
