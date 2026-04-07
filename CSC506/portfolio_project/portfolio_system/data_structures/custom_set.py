from typing import Any, List


class CustomSet:
    def __init__(self, iterable=None):
        self._data = []
        if iterable:
            for item in iterable:
                self.add(item)

    def add(self, item: Any) -> None:
        if item not in self._data:
            self._data.append(item)

    def remove(self, item: Any) -> None:
        if item in self._data:
            self._data.remove(item)
        else:
            raise KeyError(f"{item} not found in set.")

    def contains(self, item: Any) -> bool:
        return item in self._data

    def union(self, other: "CustomSet") -> "CustomSet":
        result = CustomSet(self._data)
        for item in other._data:
            result.add(item)
        return result

    def intersection(self, other: "CustomSet") -> "CustomSet":
        result = CustomSet()
        for item in self._data:
            if item in other._data:
                result.add(item)
        return result

    def difference(self, other: "CustomSet") -> "CustomSet":
        result = CustomSet()
        for item in self._data:
            if item not in other._data:
                result.add(item)
        return result

    def symmetric_difference(self, other: "CustomSet") -> "CustomSet":
        result = CustomSet()
        for item in self._data:
            if item not in other._data:
                result.add(item)
        for item in other._data:
            if item not in self._data:
                result.add(item)
        return result

    def is_subset(self, other: "CustomSet") -> bool:
        for item in self._data:
            if item not in other._data:
                return False
        return True

    def size(self) -> int:
        return len(self._data)

    def to_list(self) -> List[Any]:
        return self._data[:]

    def __str__(self) -> str:
        return "{" + ", ".join(map(str, self._data)) + "}"

    def __len__(self) -> int:
        return len(self._data)
