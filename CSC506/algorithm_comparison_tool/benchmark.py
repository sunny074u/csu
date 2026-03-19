
import random
import time
from statistics import median
from linear_search import linear_search
from binary_search import binary_search

def sample_times(fn, arr, target, reps: int) -> list[float]:
    # Warm-up
    fn(arr, target)
    samples = []
    for _ in range(reps):
        start = time.perf_counter()
        fn(arr, target)
        samples.append(time.perf_counter() - start)
    return samples

def run_bench():
    random.seed(42)
    sizes = [100, 1000, 10000]

    print("\nBenchmark (median time per search)")
    print("---------------------------------")
    print("Note: Times vary by machine; median reduces noise.\n")

    for n in sizes:
        # Use target at the end to push linear search toward worst-case behavior
        arr = random.sample(range(n * 10), n)
        target = arr[-1]

        # Linear on unsorted
        lin_samples = sample_times(linear_search, arr, target, reps=5000 if n < 10000 else 2000)
        lin_med = median(lin_samples)

        # Binary on sorted
        sarr = sorted(arr)
        bin_samples = sample_times(binary_search, sarr, target, reps=20000 if n < 10000 else 10000)
        bin_med = median(bin_samples)

        speedup = lin_med / bin_med if bin_med > 0 else float("inf")

        print(f"n={n:5d} | linear median = {lin_med*1e6:8.3f} µs | binary median = {bin_med*1e6:6.3f} µs | speedup ≈ {speedup:7.1f}x")

if __name__ == "__main__":
    run_bench()
