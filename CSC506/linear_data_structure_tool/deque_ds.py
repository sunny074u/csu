from __future__ import annotations

from typing import Generic, Iterable, Iterator, List, Optional, TypeVar

T = TypeVar("T")


class Deque(Generic[T]):
    """
    Deque implemented with a Python list.

    With a list:
      - addRear/removeRear are O(1) amortized
      - addFront/removeFront are O(n) due to shifting
    Still useful for demonstrating the ADT and its use-cases.
    """

    def __init__(self, items: Optional[Iterable[T]] = None) -> None:
        self._data: List[T] = list(items) if items is not None else []

    def add_front(self, item: T) -> None:
        self._data.insert(0, item)

    def add_rear(self, item: T) -> None:
        self._data.append(item)

    def remove_front(self) -> T:
        if self.is_empty():
            raise IndexError("remove_front from empty deque")
        return self._data.pop(0)

    def remove_rear(self) -> T:
        if self.is_empty():
            raise IndexError("remove_rear from empty deque")
        return self._data.pop()

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[T]:
        return iter(self._data)

    def __repr__(self) -> str:
        return f"Deque(front->rear {self._data})"


# --- Algorithm example using Deque: Palindrome check ---
def is_palindrome(text: str) -> bool:
    """
    Checks palindrome by comparing front and rear characters.
    Deque is a natural fit: pop from both ends.
    """
    cleaned = [c.lower() for c in text if c.isalnum()]
    d: Deque[str] = Deque(cleaned)

    while len(d) > 1:
        if d.remove_front() != d.remove_rear():
            return False
    return True