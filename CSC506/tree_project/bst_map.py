from typing import Any, List, Tuple, Optional
from binary_search_tree import BinarySearchTree


class BSTMap:
    def __init__(self) -> None:
        self.tree = BinarySearchTree()

    def put(self, key: Any, value: Any) -> None:
        self.tree.insert(key, value)

    def get(self, key: Any) -> Any:
        node = self.tree.search(key)
        if node is None:
            raise KeyError(f"Key not found: {key}")
        return node.value

    def remove(self, key: Any) -> bool:
        return self.tree.delete(key)

    def contains_key(self, key: Any) -> bool:
        return self.tree.contains(key)

    def keys(self) -> List[Any]:
        return [k for k, _ in self.tree.inorder()]

    def values(self) -> List[Any]:
        return [v for _, v in self.tree.inorder()]

    def items(self) -> List[Tuple[Any, Any]]:
        return self.tree.inorder()

    def min_item(self) -> Optional[Tuple[Any, Any]]:
        return self.tree.find_min()

    def max_item(self) -> Optional[Tuple[Any, Any]]:
        return self.tree.find_max()

    def is_balanced(self) -> bool:
        return self.tree.is_balanced()

    def pretty_print(self) -> None:
        self.tree.pretty_print()