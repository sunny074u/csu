from __future__ import annotations
from typing import Any, Optional, List, Tuple
from bst_node import BSTNode


class BinarySearchTree:
    def __init__(self) -> None:
        self.root: Optional[BSTNode] = None
        self.size: int = 0

    def insert(self, key: Any, value: Any = None) -> None:
        self.root, inserted_new = self._insert_recursive(self.root, key, value)
        if inserted_new:
            self.size += 1

    def _insert_recursive(
        self, node: Optional[BSTNode], key: Any, value: Any
    ) -> Tuple[Optional[BSTNode], bool]:
        if node is None:
            return BSTNode(key, value), True

        if key < node.key:
            node.left, inserted_new = self._insert_recursive(node.left, key, value)
        elif key > node.key:
            node.right, inserted_new = self._insert_recursive(node.right, key, value)
        else:
            node.value = value
            inserted_new = False

        return node, inserted_new

    def search(self, key: Any) -> Optional[BSTNode]:
        current = self.root
        while current is not None:
            if key == current.key:
                return current
            if key < current.key:
                current = current.left
            else:
                current = current.right
        return None

    def contains(self, key: Any) -> bool:
        return self.search(key) is not None

    def delete(self, key: Any) -> bool:
        self.root, deleted = self._delete_recursive(self.root, key)
        if deleted:
            self.size -= 1
        return deleted

    def _delete_recursive(
        self, node: Optional[BSTNode], key: Any
    ) -> Tuple[Optional[BSTNode], bool]:
        if node is None:
            return None, False

        if key < node.key:
            node.left, deleted = self._delete_recursive(node.left, key)
            return node, deleted

        if key > node.key:
            node.right, deleted = self._delete_recursive(node.right, key)
            return node, deleted

        if node.left is None and node.right is None:
            return None, True

        if node.left is None:
            return node.right, True

        if node.right is None:
            return node.left, True

        successor = self._find_min_node(node.right)
        if successor is None:
            raise RuntimeError("Successor should not be None")

        node.key = successor.key
        node.value = successor.value
        node.right, _ = self._delete_recursive(node.right, successor.key)
        return node, True

    def find_min(self) -> Optional[Tuple[Any, Any]]:
        node = self._find_min_node(self.root)
        return None if node is None else (node.key, node.value)

    def _find_min_node(self, node: Optional[BSTNode]) -> Optional[BSTNode]:
        current = node
        if current is None:
            return None
        while current.left is not None:
            current = current.left
        return current

    def find_max(self) -> Optional[Tuple[Any, Any]]:
        node = self._find_max_node(self.root)
        return None if node is None else (node.key, node.value)

    def _find_max_node(self, node: Optional[BSTNode]) -> Optional[BSTNode]:
        current = node
        if current is None:
            return None
        while current.right is not None:
            current = current.right
        return current

    def inorder(self) -> List[Tuple[Any, Any]]:
        result: List[Tuple[Any, Any]] = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(
        self, node: Optional[BSTNode], result: List[Tuple[Any, Any]]
    ) -> None:
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append((node.key, node.value))
            self._inorder_recursive(node.right, result)

    def preorder(self) -> List[Tuple[Any, Any]]:
        result: List[Tuple[Any, Any]] = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(
        self, node: Optional[BSTNode], result: List[Tuple[Any, Any]]
    ) -> None:
        if node is not None:
            result.append((node.key, node.value))
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def postorder(self) -> List[Tuple[Any, Any]]:
        result: List[Tuple[Any, Any]] = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(
        self, node: Optional[BSTNode], result: List[Tuple[Any, Any]]
    ) -> None:
        if node is not None:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append((node.key, node.value))

    def height(self) -> int:
        return self._height_recursive(self.root)

    def _height_recursive(self, node: Optional[BSTNode]) -> int:
        if node is None:
            return -1
        return 1 + max(self._height_recursive(node.left), self._height_recursive(node.right))

    def is_balanced(self) -> bool:
        balanced, _ = self._check_balance(self.root)
        return balanced

    def _check_balance(self, node: Optional[BSTNode]) -> Tuple[bool, int]:
        if node is None:
            return True, -1

        left_balanced, left_height = self._check_balance(node.left)
        right_balanced, right_height = self._check_balance(node.right)

        current_balanced = (
            left_balanced and right_balanced and abs(left_height - right_height) <= 1
        )
        return current_balanced, 1 + max(left_height, right_height)

    def unbalanced_nodes(self) -> List[Any]:
        result: List[Any] = []
        self._collect_unbalanced_nodes(self.root, result)
        return result

    def _collect_unbalanced_nodes(
        self, node: Optional[BSTNode], result: List[Any]
    ) -> int:
        if node is None:
            return -1

        left_height = self._collect_unbalanced_nodes(node.left, result)
        right_height = self._collect_unbalanced_nodes(node.right, result)

        if abs(left_height - right_height) > 1:
            result.append(node.key)

        return 1 + max(left_height, right_height)

    def is_valid_bst(self) -> bool:
        return self._validate_bst(self.root, None, None)

    def _validate_bst(
        self, node: Optional[BSTNode], min_key: Optional[Any], max_key: Optional[Any]
    ) -> bool:
        if node is None:
            return True

        if min_key is not None and node.key <= min_key:
            return False
        if max_key is not None and node.key >= max_key:
            return False

        return (
            self._validate_bst(node.left, min_key, node.key)
            and self._validate_bst(node.right, node.key, max_key)
        )

    def pretty_print(self) -> None:
        self._pretty_print_recursive(self.root, "", True)

    def _pretty_print_recursive(
        self, node: Optional[BSTNode], prefix: str, is_left: bool
    ) -> None:
        if node is not None:
            if node.right is not None:
                self._pretty_print_recursive(
                    node.right, prefix + ("│   " if is_left else "    "), False
                )

            print(prefix + ("└── " if is_left else "┌── ") + f"{node.key}:{node.value}")

            if node.left is not None:
                self._pretty_print_recursive(
                    node.left, prefix + ("    " if is_left else "│   "), True
                )