
from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterable, Iterator, List, Optional, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
    """
    Stack (LIFO) implemented with a Python list.
    Top of stack is the end of the list to keep push/pop O(1) amortized.
    """

    def __init__(self, items: Optional[Iterable[T]] = None) -> None:
        self._data: List[T] = list(items) if items is not None else []

    def push(self, item: T) -> None:
        self._data.append(item)

    def pop(self) -> T:
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self) -> T:
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._data[-1]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[T]:
        # Iterate from bottom -> top (not a requirement, just predictable)
        return iter(self._data)

    def __repr__(self) -> str:
        return f"Stack(top->bottom {list(reversed(self._data))})"


# --- Algorithm example using Stack: Balanced parentheses/brackets ---
def is_balanced(expression: str) -> bool:
    """
    Returns True if (), {}, [] are properly balanced.
    Classic stack use-case: last-opened must be the first closed.
    """
    pairs = {")": "(", "]": "[", "}": "{"}
    opens = set(pairs.values())

    s: Stack[str] = Stack()

    for ch in expression:
        if ch in opens:
            s.push(ch)
        elif ch in pairs:
            if s.is_empty():
                return False
            if s.pop() != pairs[ch]:
                return False

    return s.is_empty()