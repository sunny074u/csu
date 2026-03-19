import random
import time
from linear_search import linear_search
from binary_search import binary_search

def make_dataset(n: int, sorted_required: bool) -> list[int]:
    # Unique integers so results are clear
    data = random.sample(range(n * 10), n)
    return sorted(data) if sorted_required else data

def timed_call(fn, *args):
    start = time.perf_counter()
    result = fn(*args)
    elapsed = time.perf_counter() - start
    return result, elapsed

def main():
    print("\nSearch Algorithm Comparison Tool")
    print("--------------------------------")

    while True:
        try:
            n = int(input("\nChoose dataset size (100, 1000, 10000) or 0 to quit: ").strip())
        except ValueError:
            print("Please enter a number.")
            continue

        if n == 0:
            print("Goodbye.")
            break

        if n not in (100, 1000, 10000):
            print("Pick 100, 1000, or 10000.")
            continue

        algo = input("Choose algorithm: (L)inear or (B)inary: ").strip().lower()
        if algo not in ("l", "b"):
            print("Type L or B.")
            continue

        try:
            target = int(input("Enter an integer value to search for: ").strip())
        except ValueError:
            print("Please enter an integer.")
            continue

        if algo == "l":
            data = make_dataset(n, sorted_required=False)
            idx, secs = timed_call(linear_search, data, target)
            print(f"\nLinear Search on UNSORTED data (n={n})")
        else:
            data = make_dataset(n, sorted_required=True)
            idx, secs = timed_call(binary_search, data, target)
            print(f"\nBinary Search on SORTED data (n={n})")

        found_msg = f"FOUND at index {idx}" if idx != -1 else "NOT FOUND"
        print(f"Result: {found_msg}")
        print(f"Time: {secs * 1_000_000:.2f} µs")

        # Helpful hint for users testing “found” cases quickly
        print("\nTip: If you want a guaranteed FOUND test, try searching for one of these values:")
        print(f"First 5 values: {data[:5]}")
        print(f"Last 5 values : {data[-5:]}\n")

if __name__ == "__main__":
    main()
