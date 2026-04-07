from typing import List


def partition(arr: List[int], low: int, high: int) -> int:
    pivot = arr[high]
    i = low

    for j in range(low, high):
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1

    arr[i], arr[high] = arr[high], arr[i]
    return i


def quickselect(arr: List[int], k: int) -> int:
    """Return the kth smallest element in the list, where k is 1-based."""
    if not arr:
        raise ValueError("List cannot be empty.")
    if k < 1 or k > len(arr):
        raise ValueError("k must be between 1 and the length of the list.")

    data = arr[:]
    target_index = k - 1
    low, high = 0, len(data) - 1

    while low <= high:
        pivot_index = partition(data, low, high)

        if pivot_index == target_index:
            return data[pivot_index]
        if pivot_index < target_index:
            low = pivot_index + 1
        else:
            high = pivot_index - 1

    raise RuntimeError("Quickselect failed unexpectedly.")
