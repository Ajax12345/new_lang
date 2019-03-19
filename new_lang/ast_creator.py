import lang_exceptions, typing

class AST:
    def __init__(self, _from_loop, _delimeter = None) -> None:
        self.__dict__ = {**_from_loop.__dict__, 'delimeter':_delimeter}
    def start(self) -> None:
        pass

    @classmethod
    def create_ast(cls, _from_loop, _delimeter = None) -> typing.Any:
        _ast = cls(_from_loop, _delimeter = _delimeter)
        _ast.start()
        return _ast
