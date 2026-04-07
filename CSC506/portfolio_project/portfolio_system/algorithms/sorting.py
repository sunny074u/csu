from typing import List, Tuple


def bubble_sort_visualized(arr: List[int], show_steps: bool = True) -> Tuple[List[int], int, int]:
    """Sort a list using bubble sort and optionally print each step."""
    data = arr[:]
    n = len(data)
    comparisons = 0
    swaps = 0

    if show_steps:
        print("\nBubble Sort Visualization")
        print(f"Initial list: {data}")

    for i in range(n):
        swapped = False
        if show_steps:
            print(f"\nPass {i + 1}:")

        for j in range(0, n - i - 1):
            comparisons += 1
            if show_steps:
                print(f"  Compare {data[j]} and {data[j + 1]}", end="")

            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                swaps += 1
                swapped = True
                if show_steps:
                    print(f" -> swap -> {data}")
            else:
                if show_steps:
                    print(" -> no swap")

        if show_steps:
            print(f"After pass {i + 1}: {data}")

        if not swapped:
            if show_steps:
                print("No swaps made in this pass. List is already sorted.")
            break

    return data, comparisons, swaps
