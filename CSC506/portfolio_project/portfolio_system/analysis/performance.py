import random
import time
from typing import List

from portfolio_system.algorithms import bubble_sort_visualized, quickselect
from portfolio_system.data_structures import (
    Stack,
    Queue,
    BinarySearchTree,
    Graph,
    HashTable,
)


class PerformanceAnalyzer:
    @staticmethod
    def time_function(func, *args, repeats: int = 1, **kwargs):
        start = time.perf_counter()
        result = None
        for _ in range(repeats):
            result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = (end - start) / repeats
        return result, elapsed

    @staticmethod
    def analyze_sorting(sizes: List[int]) -> None:
        print("\nSorting Performance Analysis")
        print("-" * 50)
        print(f"{'Size':<10}{'Bubble Sort Time (s)':<25}{'Python sorted() Time (s)':<25}")

        for size in sizes:
            data = [random.randint(1, 10000) for _ in range(size)]
            _, bubble_time = PerformanceAnalyzer.time_function(bubble_sort_visualized, data, False)
            _, builtin_time = PerformanceAnalyzer.time_function(sorted, data)
            print(f"{size:<10}{bubble_time:<25.8f}{builtin_time:<25.8f}")

    @staticmethod
    def analyze_quickselect(sizes: List[int]) -> None:
        print("\nQuickselect Performance Analysis")
        print("-" * 50)
        print(f"{'Size':<10}{'Quickselect Time (s)':<25}{'Sorted[k] Time (s)':<25}")

        for size in sizes:
            data = [random.randint(1, 10000) for _ in range(size)]
            k = size // 2 if size > 1 else 1
            _, qs_time = PerformanceAnalyzer.time_function(quickselect, data, k)

            def sort_then_pick(d, k_value):
                return sorted(d)[k_value - 1]

            _, sort_pick_time = PerformanceAnalyzer.time_function(sort_then_pick, data, k)
            print(f"{size:<10}{qs_time:<25.8f}{sort_pick_time:<25.8f}")

    @staticmethod
    def analyze_data_structures() -> None:
        print("\nData Structure Demonstration Summary")
        print("-" * 50)

        stack = Stack()
        for i in range(5):
            stack.push(i)

        queue = Queue()
        for i in range(5):
            queue.enqueue(i)

        bst = BinarySearchTree()
        for value in [50, 30, 70, 20, 40, 60, 80]:
            bst.insert(value)

        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        graph.add_edge("B", "D")
        graph.add_edge("C", "E")

        ht = HashTable()
        ht.put("name", "Sunday")
        ht.put("course", "Data Structures")

        print("Stack:", stack)
        print("Queue:", queue)
        print("BST inorder traversal:", bst.inorder())
        print("Graph BFS from A:", graph.bfs("A"))
        print("Graph DFS from A:", graph.dfs("A"))
        print("HashTable get('name'):", ht.get("name"))
