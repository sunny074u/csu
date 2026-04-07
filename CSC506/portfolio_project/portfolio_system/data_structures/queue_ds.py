from collections import deque
from typing import Any


class Queue:
    def __init__(self):
        self.items = deque()

    def enqueue(self, item: Any) -> None:
        self.items.append(item)

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("Queue is empty.")
        return self.items.popleft()

    def front(self) -> Any:
        if self.is_empty():
            raise IndexError("Queue is empty.")
        return self.items[0]

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def size(self) -> int:
        return len(self.items)

    def __str__(self) -> str:
        return f"Queue({list(self.items)})"
