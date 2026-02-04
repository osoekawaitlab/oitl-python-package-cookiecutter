from collections.abc import Callable
from typing import TypeVar

_F = TypeVar("_F")

def step(pattern: str) -> Callable[[_F], _F]: ...

class _DataStore:
    scenario: dict[str, object]

data_store: _DataStore
