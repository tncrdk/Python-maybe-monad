from __future__ import annotations
from typing import Callable, Generic, TypeVar
from exceptions import UnwrapError
from abc import ABC

T = TypeVar("T")
S = TypeVar("S")

class Result(ABC, Generic[T]):
    def __init__(self) -> None:
        ...
    
    def __irshift__(self, func: Callable[[T], Result[S]]) -> Result[S]:
        ...

    def unwrap(self) -> T:
        ...
    
    def unwrap_or(self, default: T) -> T:
        ...
    
    def unwrap_or_else(self, func: Callable[[], T]) -> T:
        ...

    def expect(self, err_msg: str) -> T:
        ...
    

class Err(Result, Generic[T]):
    def __init__(self, err: Exception) -> None:
        self._err = err

    def __irshift__(self, func: Callable[[T], Result[S]]) -> Result[S]:
        return self

    def unwrap(self) -> T:
        raise self._err
    
    def unwrap_or(self, default: T) -> T:
        return default
    
    def unwrap_or_else(self, func: Callable[[], T]) -> T:
        return func()
    
    

class Ok(Result, Generic[T]):
    __match_args__ = ("_innervalue",)

    def __init__(self, value) -> None:
        self._innervalue = value

    def __irshift__(self, func: Callable[[T], Result[S]]) -> Result[S]:
        return func(self._innervalue)
    
    def unwrap(self) -> T:
        return self._innervalue
    
    def unwrap_or(self, default: T) -> T:
        return self._innervalue
    
    def unwrap_or_else(self, func: Callable[[], T]) -> T:
        return self._innervalue
