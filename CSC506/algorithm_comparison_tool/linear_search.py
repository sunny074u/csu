from typing import List, Any

def linear_search(arr: List[Any], target: Any) -> int:
    """
    Linear search (works on UNSORTED arrays).
    Returns index if found, else -1.
    """
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1