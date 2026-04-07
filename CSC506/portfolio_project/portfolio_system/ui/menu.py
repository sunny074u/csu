from typing import List

from portfolio_system.algorithms import bubble_sort_visualized, quickselect
from portfolio_system.analysis import PerformanceAnalyzer
from portfolio_system.data_structures import (
    BinarySearchTree,
    CustomSet,
    Graph,
    HashTable,
    Queue,
    Stack,
)


def get_integer_list() -> List[int]:
    raw = input("Enter integers separated by spaces: ").strip()
    return [int(x) for x in raw.split()]


def set_demo() -> None:
    print("\nCustom Set Demo")
    a = CustomSet([1, 2, 3, 4])
    b = CustomSet([3, 4, 5, 6])

    print("Set A =", a)
    print("Set B =", b)
    print("Union =", a.union(b))
    print("Intersection =", a.intersection(b))
    print("Difference (A - B) =", a.difference(b))
    print("Symmetric Difference =", a.symmetric_difference(b))


def data_structure_demo() -> None:
    print("\nData Structure Demo")

    stack = Stack()
    stack.push(10)
    stack.push(20)
    stack.push(30)
    print("Stack after pushes:", stack)
    print("Stack pop:", stack.pop())
    print("Stack now:", stack)

    queue = Queue()
    queue.enqueue(10)
    queue.enqueue(20)
    queue.enqueue(30)
    print("Queue after enqueues:", queue)
    print("Queue dequeue:", queue.dequeue())
    print("Queue now:", queue)

    bst = BinarySearchTree()
    for value in [40, 20, 60, 10, 30, 50, 70]:
        bst.insert(value)
    print("BST inorder traversal:", bst.inorder())
    print("Search 30 in BST:", bst.search(30))
    print("Search 99 in BST:", bst.search(99))

    graph = Graph()
    graph.add_edge("X", "Y")
    graph.add_edge("X", "Z")
    graph.add_edge("Y", "W")
    print("Graph adjacency:", graph)
    print("BFS from X:", graph.bfs("X"))
    print("DFS from X:", graph.dfs("X"))

    ht = HashTable()
    ht.put("id", 101)
    ht.put("name", "Portfolio")
    ht.put("topic", "Algorithms")
    print("Hash table:", ht)
    print("Get 'name':", ht.get("name"))


def performance_menu() -> None:
    print("\nPerformance Analysis")
    sizes = [10, 50, 100, 500]
    PerformanceAnalyzer.analyze_sorting(sizes)
    PerformanceAnalyzer.analyze_quickselect(sizes)
    PerformanceAnalyzer.analyze_data_structures()


def main_menu() -> None:
    while True:
        print("\n" + "=" * 60)
        print("PORTFOLIO SYSTEM MENU")
        print("=" * 60)
        print("1. Bubble Sort with Visualization")
        print("2. Quickselect (kth Smallest Element)")
        print("3. Custom Set Operations")
        print("4. Data Structures Demo")
        print("5. Performance Analysis")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            try:
                numbers = get_integer_list()
                sorted_list, comparisons, swaps = bubble_sort_visualized(numbers, True)
                print("\nFinal sorted list:", sorted_list)
                print("Comparisons:", comparisons)
                print("Swaps:", swaps)
            except ValueError:
                print("Invalid input. Please enter integers only.")

        elif choice == "2":
            try:
                numbers = get_integer_list()
                k = int(input("Enter k (1-based): "))
                result = quickselect(numbers, k)
                print(f"The {k}th smallest element is: {result}")
            except ValueError as e:
                print("Error:", e)

        elif choice == "3":
            set_demo()

        elif choice == "4":
            data_structure_demo()

        elif choice == "5":
            performance_menu()

        elif choice == "6":
            print("Exiting portfolio system.")
            break

        else:
            print("Invalid choice. Try again.")
