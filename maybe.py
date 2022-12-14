from __future__ import annotations
from typing import Generic, TypeAlias, Callable, TypeVar
from abc import ABC

T = TypeVar("T")
S = TypeVar("S")


class Maybe(ABC, Generic[T]):
    def __rshift__(self, func: Callable[[T], Maybe[S]]) -> Maybe[S]:
        ...

    def unwrap(self) -> T:
        ...

    def unwrap_or(self, default: T) -> T:
        ...

    def unwrap_or_else(self, func: Callable[[], T]) -> T:
        ...

    def expect(self, err_msg: str) -> T:
        ...

    def is_none(self) -> bool:
        ...

    def is_some(self) -> bool:
        ...

    def __str__(self) -> str:
        ...


class _Nothing(Maybe, Generic[T]):
    def __rshift__(self, func: Callable[[T], Maybe[S]]) -> Maybe[S]:
        return self

    def unwrap(self) -> T:
        raise Exception("Unwrapped empty value")

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, func: Callable[[], T]) -> T:
        return func()

    def expect(self, err_msg: str) -> T:
        raise Exception(err_msg)

    def is_none(self) -> bool:
        return True

    def is_some(self) -> bool:
        return False

    def __str__(self) -> str:
        return "Nothing"


class Some(Maybe, Generic[T]):
    __match_args__ = ("_innervalue",)

    def __init__(self, value: T) -> None:
        self._innervalue: T = value

    def __rshift__(self, func: Callable[[T], Maybe[S]]) -> Maybe[S]:
        return func(self._innervalue)

    def unwrap(self) -> T:
        return self._innervalue

    def unwrap_or(self, default: T) -> T:
        return self._innervalue

    def unwrap_or_else(self, func: Callable[[], T]) -> T:
        return self._innervalue

    def expect(self, err_msg: str) -> T:
        return self._innervalue

    def is_none(self) -> bool:
        return False

    def is_some(self) -> bool:
        return True

    def __str__(self) -> str:
        return f"Some({self._innervalue})"


Nothing = _Nothing()

if __name__ == "__main__":
    a = Some(3)

    def foo(i: int) -> Maybe[int]:
        if i != 8:
            return Some(i + 5)
        return Nothing

    # b = a >> foo >> foo >> foo
    # print(b)
    # c = b.unwrap()
    # print(c)
    match a:
        case Some(value):
            print(value)
        case other:
            print("not")
