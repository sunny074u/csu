from typing import Any


class HashTable:
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]

    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    def put(self, key: Any, value: Any) -> None:
        index = self._hash(key)
        bucket = self.table[index]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))

    def get(self, key: Any) -> Any:
        index = self._hash(key)
        bucket = self.table[index]

        for k, v in bucket:
            if k == key:
                return v

        raise KeyError(f"Key {key} not found.")

    def remove(self, key: Any) -> None:
        index = self._hash(key)
        bucket = self.table[index]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return

        raise KeyError(f"Key {key} not found.")

    def __str__(self) -> str:
        return str(self.table)
