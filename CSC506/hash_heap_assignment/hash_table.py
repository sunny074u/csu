from typing import Any, List, Optional, Tuple


class HashTable:
    """
    Hash table using separate chaining for collision handling.
    Stores key-value pairs with string keys.
    """

    def __init__(self, size: int = 211) -> None:
        if size <= 0:
            raise ValueError("Hash table size must be greater than 0.")
        self.size = size
        self.table: List[List[Tuple[str, Any]]] = [[] for _ in range(size)]
        self.count = 0

    def _hash(self, key: str) -> int:
        """
        Simple polynomial rolling hash function.
        Multiplies the running value by 31 and adds the ASCII value
        of each character, then compresses into table range.
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")

        hash_value = 0
        for char in key:
            hash_value = (hash_value * 31 + ord(char)) % self.size
        return hash_value

    def insert(self, key: str, value: Any) -> None:
        """
        Insert a key-value pair into the hash table.
        If the key already exists, update its value.
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")

        index = self._hash(key)
        bucket = self.table[index]

        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.count += 1

    def search(self, key: str) -> Optional[Any]:
        """
        Search for a key and return its value if found.
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")

        index = self._hash(key)
        bucket = self.table[index]

        for existing_key, value in bucket:
            if existing_key == key:
                return value
        return None

    def delete(self, key: str) -> bool:
        """
        Delete a key-value pair from the hash table.
        Returns True if deleted, otherwise False.
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")

        index = self._hash(key)
        bucket = self.table[index]

        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                del bucket[i]
                self.count -= 1
                return True
        return False

    def display(self) -> None:
        """
        Display non-empty buckets.
        """
        for i, bucket in enumerate(self.table):
            if bucket:
                print(f"Index {i}: {bucket}")

    def load_factor(self) -> float:
        """
        Return the load factor of the hash table.
        """
        return self.count / self.size if self.size > 0 else 0.0