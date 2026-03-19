
from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterator, Optional, TypeVar

T = TypeVar("T")


@dataclass
class _Node(Generic[T]):
    value: T
    next: Optional["_Node[T]"] = None


class LinkedList(Generic[T]):
    """
    Singly linked list.

    Operations included:
      - insert(value): inserts at end (tail) for a simple mental model
      - delete(value): deletes first occurrence
      - search(value): returns True/False
      - display(): returns a string representation
    """

    def __init__(self) -> None:
        self.head: Optional[_Node[T]] = None
        self._size: int = 0

    def insert(self, value: T) -> None:
        new_node = _Node(value)
        if self.head is None:
            self.head = new_node
            self._size += 1
            return

        cur = self.head
        while cur.next is not None:
            cur = cur.next
        cur.next = new_node
        self._size += 1

    def delete(self, value: T) -> bool:
        """
        Deletes first occurrence of value.
        Returns True if deleted, False if not found.
        """
        cur = self.head
        prev: Optional[_Node[T]] = None

        while cur is not None:
            if cur.value == value:
                if prev is None:
                    # deleting head
                    self.head = cur.next
                else:
                    prev.next = cur.next
                self._size -= 1
                return True
            prev = cur
            cur = cur.next

        return False

    def search(self, value: T) -> bool:
        cur = self.head
        while cur is not None:
            if cur.value == value:
                return True
            cur = cur.next
        return False

    def display(self) -> str:
        return " -> ".join(str(v) for v in self) if self.head else "(empty)"

    def __iter__(self) -> Iterator[T]:
        cur = self.head
        while cur is not None:
            yield cur.value
            cur = cur.next

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"LinkedList(size={self._size}, {self.display()})"


# --- Algorithm example using LinkedList: "move-to-front" heuristic for repeated searches ---
def move_to_front_search(ll: LinkedList[T], value: T) -> bool:
    """
    Searches for value. If found (not already head), moves it to front.
    This can speed up workloads with repeated access patterns.
    """
    if ll.head is None:
        return False

    if ll.head.value == value:
        return True

    prev = ll.head
    cur = ll.head.next

    while cur is not None:
        if cur.value == value:
            # detach cur
            prev.next = cur.next
            # move to front
            cur.next = ll.head
            ll.head = cur
            return True
        prev = cur
        cur = cur.next

    return False