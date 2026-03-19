from typing import List, Any

def binary_search(sorted_arr: List[Any], target: Any) -> int:
    """
    Binary search (works ONLY on SORTED arrays).
    Returns index if found, else -1.
    """
    left, right = 0, len(sorted_arr) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_val = sorted_arr[mid]

        if mid_val == target:
            return mid
        if mid_val < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
