from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional, Iterator, List


class Stack:
    """LIFO stack backed by Python list."""
    def __init__(self) -> None:
        self._data: List[Any] = []

    def push(self, x: Any) -> None:
        self._data.append(x)

    def pop(self) -> Any:
        if not self._data:
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self) -> Any:
        if not self._data:
            raise IndexError("peek from empty stack")
        return self._data[-1]

    def __len__(self) -> int:
        return len(self._data)

    def to_list(self) -> List[Any]:
        return list(self._data)


class Queue:
    """
    FIFO queue implemented as a circular buffer to keep enqueue/dequeue O(1) amortized.
    (Avoids O(n) cost of popping from the front of a Python list.)
    """
    def __init__(self, initial_capacity: int = 8) -> None:
        self._cap = max(8, initial_capacity)
        self._buf: List[Optional[Any]] = [None] * self._cap
        self._head = 0
        self._tail = 0
        self._size = 0

    def enqueue(self, x: Any) -> None:
        if self._size == self._cap:
            self._grow()
        self._buf[self._tail] = x
        self._tail = (self._tail + 1) % self._cap
        self._size += 1

    def dequeue(self) -> Any:
        if self._size == 0:
            raise IndexError("dequeue from empty queue")
        x = self._buf[self._head]
        self._buf[self._head] = None
        self._head = (self._head + 1) % self._cap
        self._size -= 1
        return x

    def peek(self) -> Any:
        if self._size == 0:
            raise IndexError("peek from empty queue")
        return self._buf[self._head]

    def _grow(self) -> None:
        new_cap = self._cap * 2
        new_buf: List[Optional[Any]] = [None] * new_cap
        for i in range(self._size):
            new_buf[i] = self._buf[(self._head + i) % self._cap]
        self._buf = new_buf
        self._cap = new_cap
        self._head = 0
        self._tail = self._size

    def __len__(self) -> int:
        return self._size

    def to_list(self) -> List[Any]:
        return [self._buf[(self._head + i) % self._cap] for i in range(self._size)]


@dataclass
class _Node:
    value: Any
    next: Optional["_Node"] = None


class SinglyLinkedList:
    """Singly linked list with head/tail pointers."""
    def __init__(self) -> None:
        self.head: Optional[_Node] = None
        self.tail: Optional[_Node] = None
        self._size = 0

    def insert_front(self, x: Any) -> None:
        node = _Node(x, self.head)
        self.head = node
        if self.tail is None:
            self.tail = node
        self._size += 1

    def insert_back(self, x: Any) -> None:
        node = _Node(x, None)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self._size += 1

    def delete_value(self, x: Any) -> bool:
        """Delete first occurrence of x. Returns True if deleted."""
        prev: Optional[_Node] = None
        cur = self.head
        while cur is not None:
            if cur.value == x:
                if prev is None:
                    self.head = cur.next
                else:
                    prev.next = cur.next
                if cur == self.tail:
                    self.tail = prev
                self._size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    def search(self, x: Any) -> bool:
        cur = self.head
        while cur is not None:
            if cur.value == x:
                return True
            cur = cur.next
        return False

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        cur = self.head
        while cur is not None:
            yield cur.value
            cur = cur.next

    def to_list(self) -> List[Any]:
        return list(iter(self))
