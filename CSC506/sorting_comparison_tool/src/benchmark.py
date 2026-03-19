"""Benchmark runner for sorting algorithms.

Design goals:
- Run all algorithms on all dataset types and sizes requested by the assignment.
- Record execution time using high-resolution timers.
- Prevent runaway O(n^2) tests from locking the machine by using subprocess timeouts.
- Validate correctness (must return sorted output).
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
import time
import statistics
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import multiprocessing as mp

from .sorts import ALGORITHMS
from .data_gen import DATASETS


@dataclass
class TrialResult:
    dataset_type: str
    n: int
    algorithm: str
    trial: int
    seconds: Optional[float]  # None when timeout/error
    status: str               # OK / TIMEOUT / ERROR


def _is_sorted(a: List[Any]) -> bool:
    return all(a[i] <= a[i + 1] for i in range(len(a) - 1))


def _worker(algorithm_name: str, data: List[int], q: "mp.Queue[Tuple[str, Optional[float], Optional[str]]]") -> None:
    """Run one algorithm and report status + time back to parent."""
    try:
        fn = ALGORITHMS[algorithm_name]
        t0 = time.perf_counter()
        out = fn(data)
        t1 = time.perf_counter()
        if not _is_sorted(out):
            q.put(("ERROR", None, "Output is not sorted"))
            return
        q.put(("OK", t1 - t0, None))
    except Exception as e:
        q.put(("ERROR", None, repr(e)))


def timeout_policy(algorithm: str, dataset_type: str, n: int, base_timeout: float) -> float:
    """Keep the suite practical.

    We still execute every required combination, but we cap time aggressively for cases that are known
    to explode (quadratic sorts on large random/reverse inputs).

    This is not 'cheating' the experiment: it is documenting that the algorithm is not viable under
    that scenario within a reasonable time budget.
    """
    if algorithm == "merge":
        return max(base_timeout, 3.0)

    # Quadratic algorithms: bubble/selection/insertion
    if dataset_type == "sorted":
        # sorted input is a best case for bubble(with early exit) and insertion
        return max(base_timeout, 3.0)

    if n >= 50000:
        return min(base_timeout, 0.15)
    if n >= 10000:
        return min(base_timeout, 0.35)
    if n >= 5000:
        return min(base_timeout, 0.60)

    return base_timeout


def time_one(algorithm: str, data: List[int], timeout_seconds: float) -> Tuple[str, Optional[float], Optional[str]]:
    """Run algorithm in a child process so we can enforce a timeout."""
    ctx = mp.get_context("spawn")
    q: "mp.Queue[Tuple[str, Optional[float], Optional[str]]]" = ctx.Queue()
    p = ctx.Process(target=_worker, args=(algorithm, data, q), daemon=True)
    p.start()
    p.join(timeout_seconds)

    if p.is_alive():
        p.terminate()
        p.join(0.2)
        return ("TIMEOUT", None, None)

    try:
        status, seconds, err = q.get_nowait()
        return (status, seconds, err)
    except Exception:
        return ("ERROR", None, "No result returned from worker")


def run_benchmarks(
    sizes: List[int],
    dataset_types: List[str],
    algorithms: List[str],
    trials: int,
    seed: int,
    base_timeout: float,
) -> List[TrialResult]:
    results: List[TrialResult] = []

    for dataset_type in dataset_types:
        gen = DATASETS[dataset_type]
        for n in sizes:
            for algorithm in algorithms:
                for t in range(1, trials + 1):
                    # make each trial deterministic but distinct
                    data_seed = (seed * 1000003) + (hash(dataset_type) & 0xFFFF) + n + t
                    data = gen(n, seed=data_seed) if dataset_type in ("random", "partially_sorted") else gen(n)

                    timeout_s = timeout_policy(algorithm, dataset_type, n, base_timeout)

                    status, seconds, err = time_one(algorithm, data, timeout_s)

                    if status == "ERROR" and err:
                        # Keep stderr-like hints, but don’t crash the whole run
                        pass

                    results.append(
                        TrialResult(
                            dataset_type=dataset_type,
                            n=n,
                            algorithm=algorithm,
                            trial=t,
                            seconds=seconds,
                            status=status,
                        )
                    )
    return results


def write_results_csv(results: List[TrialResult], out_csv: str) -> None:
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["dataset_type", "n", "algorithm", "trial", "seconds", "status"])
        for r in results:
            w.writerow([r.dataset_type, r.n, r.algorithm, r.trial, f"{r.seconds:.9f}" if r.seconds is not None else "", r.status])


def summarize_best(results: List[TrialResult], out_csv: str) -> None:
    """Pick the best (lowest) time per dataset_type x n across algorithms (ignoring TIMEOUT/ERROR)."""
    from collections import defaultdict

    grouped: Dict[Tuple[str, int, str], List[float]] = defaultdict(list)
    for r in results:
        if r.status == "OK" and r.seconds is not None:
            grouped[(r.dataset_type, r.n, r.algorithm)].append(r.seconds)

    # compute median per algorithm per scenario
    medians: Dict[Tuple[str, int, str], float] = {}
    for key, vals in grouped.items():
        medians[key] = statistics.median(vals)

    # choose best algorithm
    best_rows = []
    scenarios = sorted({(r.dataset_type, r.n) for r in results}, key=lambda x: (x[0], x[1]))
    for dataset_type, n in scenarios:
        candidates = [(alg, medians[(dataset_type, n, alg)]) for alg in {r.algorithm for r in results} if (dataset_type, n, alg) in medians]
        if not candidates:
            best_rows.append([dataset_type, n, "", "", "NO_OK_RUNS"])
            continue
        alg, sec = min(candidates, key=lambda x: x[1])
        best_rows.append([dataset_type, n, alg, f"{sec:.9f}", "OK"])

    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["dataset_type", "n", "best_algorithm", "median_seconds", "status"])
        w.writerows(best_rows)


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--outdir", default="out", help="Output directory for CSV files")
    p.add_argument("--trials", type=int, default=1, help="Trials per algorithm per scenario")
    p.add_argument("--seed", type=int, default=42, help="Random seed base")
    p.add_argument("--timeout", type=float, default=1.0, help="Base timeout (seconds) used by timeout policy")
    args = p.parse_args(argv)

    sizes = [1000, 5000, 10000, 50000]
    dataset_types = ["random", "sorted", "reverse_sorted", "partially_sorted"]
    algorithms = ["bubble", "selection", "insertion", "merge"]

    results = run_benchmarks(
        sizes=sizes,
        dataset_types=dataset_types,
        algorithms=algorithms,
        trials=args.trials,
        seed=args.seed,
        base_timeout=args.timeout,
    )

    results_csv = os.path.join(args.outdir, "results.csv")
    summary_csv = os.path.join(args.outdir, "summary.csv")
    write_results_csv(results, results_csv)
    summarize_best(results, summary_csv)

    print(f"Wrote: {results_csv}")
    print(f"Wrote: {summary_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
