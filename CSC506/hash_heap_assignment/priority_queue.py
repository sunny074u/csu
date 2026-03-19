from typing import Any, List, Optional, Tuple


class PriorityQueueMaxHeap:
    """
    Priority queue implemented using a binary max-heap.
    Higher priority values are served first.
    """

    def __init__(self) -> None:
        self.heap: List[Tuple[int, Any]] = []

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    def _parent(self, index: int) -> int:
        return (index - 1) // 2

    def _left_child(self, index: int) -> int:
        return 2 * index + 1

    def _right_child(self, index: int) -> int:
        return 2 * index + 2

    def _swap(self, i: int, j: int) -> None:
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, priority: int, value: Any) -> None:
        """
        Insert a new item into the priority queue.
        """
        if not isinstance(priority, int):
            raise TypeError("Priority must be an integer.")

        self.heap.append((priority, value))
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index: int) -> None:
        """
        Restore heap property after insertion.
        """
        while index > 0:
            parent = self._parent(index)
            if self.heap[index][0] > self.heap[parent][0]:
                self._swap(index, parent)
                index = parent
            else:
                break

    def peek(self) -> Optional[Tuple[int, Any]]:
        """
        Return the highest-priority item without removing it.
        """
        if self.is_empty():
            return None
        return self.heap[0]

    def extract_max(self) -> Optional[Tuple[int, Any]]:
        """
        Remove and return the highest-priority item.
        """
        if self.is_empty():
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def _heapify_down(self, index: int) -> None:
        """
        Restore heap property after removal.
        """
        size = len(self.heap)

        while True:
            largest = index
            left = self._left_child(index)
            right = self._right_child(index)

            if left < size and self.heap[left][0] > self.heap[largest][0]:
                largest = left

            if right < size and self.heap[right][0] > self.heap[largest][0]:
                largest = right

            if largest != index:
                self._swap(index, largest)
                index = largest
            else:
                break

    def search(self, value: Any) -> Optional[Tuple[int, Any]]:
        """
        Search for an item by value.
        Returns the first matching (priority, value) pair if found.
        """
        for item in self.heap:
            if item[1] == value:
                return item
        return None

    def delete(self, value: Any) -> bool:
        """
        Delete the first occurrence of a value from the heap.
        Returns True if deleted, otherwise False.
        """
        for i, item in enumerate(self.heap):
            if item[1] == value:
                last_item = self.heap.pop()

                if i < len(self.heap):
                    self.heap[i] = last_item
                    parent = self._parent(i) if i > 0 else 0

                    if i > 0 and self.heap[i][0] > self.heap[parent][0]:
                        self._heapify_up(i)
                    else:
                        self._heapify_down(i)

                return True
        return False

    def display(self) -> None:
        """
        Display the internal heap list.
        """
        print(self.heap)