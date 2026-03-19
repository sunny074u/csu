import random
import string
import timeit

from binary_search_tree import BinarySearchTree
from bst_map import BSTMap
from list_map import ListMap


def build_numeric_test_data(n: int = 50) -> list[int]:
    return random.sample(range(1, 500), n)


def build_string_test_data(n: int = 20) -> list[str]:
    words = set()
    while len(words) < n:
        words.add("".join(random.choices(string.ascii_lowercase, k=5)))
    return list(words)


def demonstrate_bst() -> None:
    print("=" * 70)
    print("BST DEMONSTRATION")
    print("=" * 70)

    bst = BinarySearchTree()
    numbers = build_numeric_test_data(50)

    for num in numbers:
        bst.insert(num, f"value_{num}")

    print(f"Inserted items: {len(numbers)}")
    print(f"Tree size: {bst.size}")
    print(f"Tree height: {bst.height()}")
    print(f"BST valid: {bst.is_valid_bst()}")
    print(f"Balanced: {bst.is_balanced()}")
    print(f"Unbalanced nodes: {bst.unbalanced_nodes()[:10]}")
    print(f"Minimum item: {bst.find_min()}")
    print(f"Maximum item: {bst.find_max()}")

    print("\nSearch examples:")
    for target in [numbers[0], numbers[10], 9999]:
        node = bst.search(target)
        if node:
            print(f"Found {target} -> {node.value}")
        else:
            print(f"{target} not found")

    print("\nTraversal examples:")
    print("In-order:", bst.inorder()[:15])
    print("Pre-order:", bst.preorder()[:15])
    print("Post-order:", bst.postorder()[:15])

    print("\nTree before deletions:")
    bst.pretty_print()

    delete_targets = numbers[:3]
    print("\nDeleting:", delete_targets)
    for target in delete_targets:
        print(f"Delete {target}: {bst.delete(target)}")

    print("\nTree after deletions:")
    bst.pretty_print()


def demonstrate_bst_map() -> None:
    print("\n" + "=" * 70)
    print("BST MAP DEMONSTRATION")
    print("=" * 70)

    numeric_map = BSTMap()
    for i in range(1, 31):
        numeric_map.put(i, i * i)

    print("Contains key 10:", numeric_map.contains_key(10))
    print("Value at key 10:", numeric_map.get(10))
    print("Minimum item:", numeric_map.min_item())
    print("Maximum item:", numeric_map.max_item())
    print("Sorted items:", numeric_map.items()[:15])

    numeric_map.remove(10)
    print("Contains key 10 after removal:", numeric_map.contains_key(10))

    print("\nNumeric map tree:")
    numeric_map.pretty_print()

    print("\nSeparate string-key map:")
    string_map = BSTMap()
    for idx, word in enumerate(build_string_test_data(20)):
        string_map.put(word, {"index": idx, "length": len(word)})

    print("Sorted string keys:", string_map.keys())
    print("Minimum string key:", string_map.min_item())
    print("Maximum string key:", string_map.max_item())


def performance_analysis() -> None:
    print("\n" + "=" * 70)
    print("PERFORMANCE ANALYSIS")
    print("=" * 70)

    random.seed(42)
    size = 5000
    keys = random.sample(range(1, 100000), size)
    search_keys = random.sample(keys, 1000)

    tree_map = BSTMap()
    list_map = ListMap()

    for key in keys:
        tree_map.put(key, key * 10)
        list_map.put(key, key * 10)

    def tree_lookup():
        for key in search_keys:
            tree_map.get(key)

    def list_lookup():
        for key in search_keys:
            list_map.get(key)

    tree_time = timeit.timeit(tree_lookup, number=10)
    list_time = timeit.timeit(list_lookup, number=10)

    print(f"BST-based map lookup time:  {tree_time:.6f} seconds")
    print(f"List-based map lookup time: {list_time:.6f} seconds")

    if tree_time < list_time:
        print(f"Tree-based map was about {list_time / tree_time:.2f}x faster.")
    else:
        print("List-based map was faster in this run, likely due to tree shape or test conditions.")


def main() -> None:
    random.seed(7)
    demonstrate_bst()
    demonstrate_bst_map()
    performance_analysis()
    print("\nProject completed successfully.")


if __name__ == "__main__":
    main()