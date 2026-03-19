"""Dataset generators for sorting benchmarks.

Generates 4 dataset types:
- random: random integers
- sorted: already sorted ascending
- reverse_sorted: descending
- partially_sorted: mostly sorted with a controlled amount of disorder
"""

from __future__ import annotations
from typing import List
import random


def random_data(n: int, seed: int | None = None) -> List[int]:
    r = random.Random(seed)
    # Wider range reduces duplicates a bit, but duplicates are allowed.
    return [r.randint(0, max(10, n * 10)) for _ in range(n)]


def sorted_data(n: int) -> List[int]:
    return list(range(n))


def reverse_sorted_data(n: int) -> List[int]:
    return list(range(n, 0, -1))


def partially_sorted_data(n: int, seed: int | None = None, disorder_fraction: float = 0.10) -> List[int]:
    """Start sorted, then perform swaps to introduce disorder.

    disorder_fraction = 0.10 means ~10% of positions will be involved in swaps.
    """
    r = random.Random(seed)
    a = list(range(n))
    swaps = max(1, int(n * disorder_fraction))
    for _ in range(swaps):
        i = r.randrange(n)
        j = r.randrange(n)
        a[i], a[j] = a[j], a[i]
    return a


DATASETS = {
    "random": random_data,
    "sorted": lambda n, seed=None: sorted_data(n),
    "reverse_sorted": lambda n, seed=None: reverse_sorted_data(n),
    "partially_sorted": lambda n, seed=None: partially_sorted_data(n, seed=seed, disorder_fraction=0.10),
}
