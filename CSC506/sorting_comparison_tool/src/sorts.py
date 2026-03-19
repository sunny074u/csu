"""Sorting algorithms for benchmarking.

Each function returns a NEW sorted list and does not mutate the input.
Designed for clarity and correctness first, with a few practical optimizations
(e.g., early exit in bubble sort).
"""

from __future__ import annotations
from typing import List, TypeVar

T = TypeVar("T")


def bubble_sort(arr: List[T]) -> List[T]:
    a = list(arr)
    n = len(a)
    if n < 2:
        return a

    for i in range(n - 1):
        swapped = False
        # after each pass, the largest element in the remaining range is at the end
        for j in range(0, n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def selection_sort(arr: List[T]) -> List[T]:
    a = list(arr)
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
    return a


def insertion_sort(arr: List[T]) -> List[T]:
    a = list(arr)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(arr: List[T]) -> List[T]:
    a = list(arr)
    n = len(a)
    if n < 2:
        return a

    mid = n // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])
    return _merge(left, right)


def _merge(left: List[T], right: List[T]) -> List[T]:
    merged: List[T] = []
    i = j = 0
    while i < len(left) and j < len(right):
        # stable merge: left item wins ties
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    if i < len(left):
        merged.extend(left[i:])
    if j < len(right):
        merged.extend(right[j:])
    return merged


ALGORITHMS = {
    "bubble": bubble_sort,
    "selection": selection_sort,
    "insertion": insertion_sort,
    "merge": merge_sort,
}
