from typing import Any


class Stack:
    def __init__(self):
        self.items = []

    def push(self, item: Any) -> None:
        self.items.append(item)

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("Stack is empty.")
        return self.items.pop()

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("Stack is empty.")
        return self.items[-1]

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def size(self) -> int:
        return len(self.items)

    def __str__(self) -> str:
        return f"Stack({self.items})"
