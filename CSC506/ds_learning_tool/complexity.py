from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class Complexity:
    time: str
    space: str


# Big-O summaries (typical implementations)
# Note: Stack uses dynamic array -> amortized O(1) push/pop.
# Queue here is circular buffer -> amortized O(1) enqueue/dequeue.
# Linked list search/delete-by-value is O(n).
COMPLEXITIES: Dict[str, Dict[str, Complexity]] = {
    "Stack": {
        "insert (push)": Complexity("O(1) amortized", "O(1) extra"),
        "delete (pop)": Complexity("O(1)", "O(1) extra"),
        "search": Complexity("O(n)", "O(1) extra"),
        "peek": Complexity("O(1)", "O(1) extra"),
    },
    "Queue": {
        "insert (enqueue)": Complexity("O(1) amortized", "O(1) extra"),
        "delete (dequeue)": Complexity("O(1)", "O(1) extra"),
        "search": Complexity("O(n)", "O(1) extra"),
        "peek": Complexity("O(1)", "O(1) extra"),
    },
    "Linked List": {
        "insert front": Complexity("O(1)", "O(1) extra"),
        "insert back": Complexity("O(1)", "O(1) extra"),
        "delete (by value)": Complexity("O(n)", "O(1) extra"),
        "search": Complexity("O(n)", "O(1) extra"),
    },
}


def predict(ds_name: str, operation: str) -> Tuple[str, str]:
    if ds_name not in COMPLEXITIES or operation not in COMPLEXITIES[ds_name]:
        return ("Unknown", "Unknown")
    c = COMPLEXITIES[ds_name][operation]
    return (c.time, c.space)
