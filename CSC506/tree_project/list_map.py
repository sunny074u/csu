from typing import Any, List, Tuple


class ListMap:
    def __init__(self) -> None:
        self.data: List[Tuple[Any, Any]] = []

    def put(self, key: Any, value: Any) -> None:
        for i, (k, _) in enumerate(self.data):
            if k == key:
                self.data[i] = (key, value)
                return
        self.data.append((key, value))

    def get(self, key: Any) -> Any:
        for k, v in self.data:
            if k == key:
                return v
        raise KeyError(f"Key not found: {key}")