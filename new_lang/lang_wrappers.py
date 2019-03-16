import typing, functools
import collections.abc

def to_iter(_flag:bool) -> typing.Callable:
    def _inner(_f:typing.Callable) -> typing.Callable:
        @functools.wraps(_f)
        def _wrapper(*args, **kwargs) -> typing.Any:
            _result = _f(*args, **kwargs)
            return _result if not _flag else iter([iter(c) for c in _f(*args, **kwargs)])
            
        return _wrapper
    return _inner


def is_iterator(_f:typing.Callable) -> typing.Callable:
    @functools.wraps(_f)
    def _wrapper(*args, _iter) -> typing.Any:
        if not isinstance(_iter, collections.abc.Iterator):
            raise TypeError(f"'{_f.__name__}' requires an iterator, got {type(_iter).__name__}")
        return _f(*args, _iter)
    return _wrapper
