import random
import string
import time
from typing import Any, List, Optional, Tuple

from hash_table import HashTable
from priority_queue import PriorityQueueMaxHeap


def linear_search(data: List[Tuple[str, Any]], target_key: str) -> Optional[Any]:
    """
    Simple linear search for comparison with hash table search.
    """
    for key, value in data:
        if key == target_key:
            return value
    return None


def generate_random_key(length: int = 8) -> str:
    """
    Generate a random string key.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def build_test_data(n: int = 100) -> List[Tuple[str, int]]:
    """
    Build a dataset of unique string keys and integer values.
    """
    data = []
    used_keys = set()

    while len(data) < n:
        key = generate_random_key()
        if key not in used_keys:
            used_keys.add(key)
            value = random.randint(1, 1000)
            data.append((key, value))

    return data


def demo_hash_table(data: List[Tuple[str, int]]) -> None:
    print("\n" + "=" * 60)
    print("HASH TABLE DEMO")
    print("=" * 60)

    # Smaller size chosen intentionally to increase likelihood of collisions
    hash_table = HashTable(size=53)

    for key, value in data:
        hash_table.insert(key, value)

    print(f"Inserted {len(data)} items into the hash table.")
    print(f"Load factor: {hash_table.load_factor():.2f}")

    existing_key = data[10][0]
    print(f"\nSearching for existing key: {existing_key}")
    print("Result:", hash_table.search(existing_key))

    missing_key = "NOT_IN_TABLE"
    print(f"\nSearching for missing key: {missing_key}")
    print("Result:", hash_table.search(missing_key))

    print(f"\nDeleting existing key: {existing_key}")
    print("Deleted:", hash_table.delete(existing_key))
    print("Search after delete:", hash_table.search(existing_key))


def demo_priority_queue(data: List[Tuple[str, int]]) -> None:
    print("\n" + "=" * 60)
    print("PRIORITY QUEUE DEMO")
    print("=" * 60)

    pq = PriorityQueueMaxHeap()

    for key, value in data:
        pq.insert(priority=value, value=key)

    print(f"Inserted {len(data)} items into the priority queue.")

    print("\nTop item using peek():")
    print(pq.peek())

    print("\nExtracting top 5 highest-priority items:")
    for _ in range(5):
        print(pq.extract_max())

    sample_value = data[20][0]
    print(f"\nSearching for item value: {sample_value}")
    print("Result:", pq.search(sample_value))

    print(f"\nDeleting item value: {sample_value}")
    print("Deleted:", pq.delete(sample_value))
    print("Search after delete:", pq.search(sample_value))


def performance_test(data: List[Tuple[str, int]]) -> None:
    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON")
    print("HASH TABLE SEARCH VS LINEAR SEARCH")
    print("=" * 60)

    hash_table = HashTable(size=211)

    for key, value in data:
        hash_table.insert(key, value)

    search_keys = [item[0] for item in random.sample(data, min(50, len(data)))]

    start_hash = time.perf_counter()
    for key in search_keys:
        hash_table.search(key)
    end_hash = time.perf_counter()

    start_linear = time.perf_counter()
    for key in search_keys:
        linear_search(data, key)
    end_linear = time.perf_counter()

    hash_time = end_hash - start_hash
    linear_time = end_linear - start_linear

    print(f"Number of data items: {len(data)}")
    print(f"Number of searches performed: {len(search_keys)}")
    print(f"Hash table search time: {hash_time:.8f} seconds")
    print(f"Linear search time:     {linear_time:.8f} seconds")

    if hash_time < linear_time:
        print("Result: Hash table search was faster.")
    elif linear_time < hash_time:
        print("Result: Linear search was faster in this run.")
    else:
        print("Result: Both methods took the same time in this run.")


def main() -> None:
    random.seed(42)  # Keeps test results reproducible
    data = build_test_data(100)

    demo_hash_table(data)
    demo_priority_queue(data)
    performance_test(data)

    print("\n" + "=" * 60)
    print("PROGRAM COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()