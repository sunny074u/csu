from __future__ import annotations

from typing import Generic, Iterable, Iterator, List, Optional, TypeVar

T = TypeVar("T")


class Queue(Generic[T]):
    """
    Queue (FIFO) implemented with a Python list.

    Note: dequeue from the front uses pop(0) which is O(n) because elements shift.
    This matches the assignment requirement (Python lists). We'll call this out in analysis.
    """

    def __init__(self, items: Optional[Iterable[T]] = None) -> None:
        self._data: List[T] = list(items) if items is not None else []

    def enqueue(self, item: T) -> None:
        self._data.append(item)

    def dequeue(self) -> T:
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._data.pop(0)

    def front(self) -> T:
        if self.is_empty():
            raise IndexError("front from empty queue")
        return self._data[0]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[T]:
        return iter(self._data)

    def __repr__(self) -> str:
        return f"Queue(front->rear {self._data})"


# --- Algorithm example using Queue: Breadth-First Search (BFS) on an unweighted graph ---
def bfs_order(graph: dict[str, list[str]], start: str) -> list[str]:
    """
    Returns nodes in BFS visit order from 'start'.
    BFS is a queue problem: process in the same order discovered.
    """
    if start not in graph:
        return []

    q: Queue[str] = Queue([start])
    visited: set[str] = {start}
    order: list[str] = []

    while not q.is_empty():
        node = q.dequeue()
        order.append(node)
        for nbr in graph.get(node, []):
            if nbr not in visited:
                visited.add(nbr)
                q.enqueue(nbr)

    return order