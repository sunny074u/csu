from __future__ import annotations
import time
import random
import csv
from dataclasses import dataclass
from typing import Callable, List, Tuple, Dict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from structures import Stack, Queue, SinglyLinkedList


@dataclass
class BenchCase:
    ds_name: str
    op_name: str
    run: Callable[[int], None]  # function that runs operation at size n
    expected: str               # "O(1)" or "O(n)" (for this assignment)


def _time_once(fn: Callable[[], None]) -> float:
    t0 = time.perf_counter()
    fn()
    return time.perf_counter() - t0


def _median_time(fn: Callable[[], None], reps: int = 25) -> float:
    times = [_time_once(fn) for _ in range(reps)]
    return float(np.median(times))


def build_cases() -> List[BenchCase]:
    cases: List[BenchCase] = []

    # Stack: push (amortized O(1)), search O(n)
    def stack_push(n: int) -> None:
        s = Stack()
        for i in range(n):
            s.push(i)
        s.push(-1)

    def stack_search(n: int) -> None:
        s = Stack()
        for i in range(n):
            s.push(i)
        # search by scanning list representation
        _ = (-1 in s.to_list())

    cases.append(BenchCase("Stack", "push", stack_push, "O(1)"))
    cases.append(BenchCase("Stack", "search", stack_search, "O(n)"))

    # Queue: enqueue O(1) amortized, search O(n)
    def queue_enqueue(n: int) -> None:
        q = Queue()
        for i in range(n):
            q.enqueue(i)
        q.enqueue(-1)

    def queue_search(n: int) -> None:
        q = Queue()
        for i in range(n):
            q.enqueue(i)
        _ = (-1 in q.to_list())

    cases.append(BenchCase("Queue", "enqueue", queue_enqueue, "O(1)"))
    cases.append(BenchCase("Queue", "search", queue_search, "O(n)"))

    # Linked list: insert_back O(1), search O(n), delete_value O(n)
    def ll_insert_back(n: int) -> None:
        ll = SinglyLinkedList()
        for i in range(n):
            ll.insert_back(i)
        ll.insert_back(-1)

    def ll_search(n: int) -> None:
        ll = SinglyLinkedList()
        for i in range(n):
            ll.insert_back(i)
        _ = ll.search(-1)

    def ll_delete(n: int) -> None:
        ll = SinglyLinkedList()
        for i in range(n):
            ll.insert_back(i)
        _ = ll.delete_value(n - 1)

    cases.append(BenchCase("Linked List", "insert_back", ll_insert_back, "O(1)"))
    cases.append(BenchCase("Linked List", "search", ll_search, "O(n)"))
    cases.append(BenchCase("Linked List", "delete_value", ll_delete, "O(n)"))

    return cases


def infer_growth(ns: List[int], ts: List[float]) -> str:
    """
    Very simple classifier:
      If time roughly scales with n -> O(n)
      If time roughly flat -> O(1)
    Uses slope of log-log fit: t = a * n^k => k ~ 0 for O(1), k ~ 1 for O(n)
    """
    x = np.log(np.array(ns, dtype=float))
    y = np.log(np.array(ts, dtype=float) + 1e-12)
    k, b = np.polyfit(x, y, 1)
    if k < 0.35:
        return "O(1)"
    return "O(n)"


def main(out_dir: str = "outputs") -> None:
    random.seed(7)
    ns = [100, 500, 1_000, 5_000, 10_000, 25_000]
    reps = 15

    rows = []
    growth_rows = []

    for case in build_cases():
        times = []
        for n in ns:
            t = _median_time(lambda: case.run(n), reps=reps)
            times.append(t)
            rows.append({"ds": case.ds_name, "op": case.op_name, "n": n, "seconds": t, "expected": case.expected})

        inferred = infer_growth(ns, times)
        growth_rows.append({"ds": case.ds_name, "op": case.op_name, "expected": case.expected, "inferred": inferred,
                            "match": inferred == case.expected})

    df = pd.DataFrame(rows)
    acc = pd.DataFrame(growth_rows)

    import os
    os.makedirs(out_dir, exist_ok=True)
    df.to_csv(f"{out_dir}/benchmark_results.csv", index=False)
    acc.to_csv(f"{out_dir}/prediction_accuracy.csv", index=False)

    # Charts (one per DS for readability)
    for ds in df["ds"].unique():
        sub = df[df["ds"] == ds]
        plt.figure()
        for op in sub["op"].unique():
            ssub = sub[sub["op"] == op].sort_values("n")
            plt.plot(ssub["n"], ssub["seconds"], marker="o", label=op)
        plt.xlabel("n (size)")
        plt.ylabel("time (seconds)")
        plt.title(f"{ds}: measured times vs size")
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"{out_dir}/chart_{ds.lower().replace(' ', '')}.png", dpi=200)
        plt.close()

    # Accuracy overview chart
    plt.figure()
    counts = acc.groupby(["ds", "match"]).size().unstack(fill_value=0)
    counts.plot(kind="bar")  # matplotlib will attach to current figure
    plt.xlabel("Data structure")
    plt.ylabel("Number of operations")
    plt.title("Prediction accuracy: expected vs inferred growth")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/accuracy_overview.png", dpi=200)
    plt.close()

    print("Saved:")
    print(f"- {out_dir}/benchmark_results.csv")
    print(f"- {out_dir}/prediction_accuracy.csv")
    print(f"- {out_dir}/chart_*.png and {out_dir}/accuracy_overview.png")


if __name__ == "__main__":
    main()
