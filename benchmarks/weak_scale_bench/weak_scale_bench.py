#!/usr/bin/env python3
"""
Task 22 - Weak-scaling benchmark (Python multiprocessing).

Workload : midpoint-rule integration of 4/(1+x^2) on [0,1]  (= pi).
Weak scaling : every worker integrates exactly K intervals, so the global problem has N = P*K intervals.
Optional injected serial phase (--serial-frac f) : the parent process first integrates K_s = f/(1-f)*K intervals
          (constant, independent of P), which makes the *true* serial fraction of the P-worker run equal to f.
          Useful for validating fit_gustafson.py (the fit should recover ~f).

Timed region = serial phase + task dispatch + parallel integration + reduction (pool creation and one warm-up run are NOT timed).

Output CSV columns: threads,run,k_per_worker,serial_frac_injected,wall_s,pi_estimate

Usage
    python3 weak_scale_bench.py                       # 1,2,4,... up to hardware threads, 5 runs each
    python3 weak_scale_bench.py --threads 1,2,4,8 --runs 5 --k 30000000 --out ../results.csv
    python3 weak_scale_bench.py --serial-frac 0.05    # validation run
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")       # keep numpy single-threaded inside each worker
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import argparse
import csv
import multiprocessing as mp
import sys
import time

import numpy as np

CHUNK = 2_000_000


def integrate(args):
    """Midpoint rule for intervals [start, start+count) out of total_n."""
    start, count, total_n = args
    h = 1.0 / total_n
    acc, i, end = 0.0, start, start + count
    while i < end:
        m = min(CHUNK, end - i)
        x = (np.arange(i, i + m, dtype=np.float64) + 0.5) * h
        acc += float(np.sum(4.0 / (1.0 + x * x)))
        i += m
    return acc * h


def hw_threads():
    try:
        return len(os.sched_getaffinity(0))
    except AttributeError:
        return os.cpu_count() or 1


def default_thread_list():
    n, out, p = hw_threads(), [], 1
    while p < n:
        out.append(p)
        p *= 2
    out.append(n)
    return sorted(set(out))


def run_once(pool, P, k, k_serial):
    n_total = P * k
    t0 = time.perf_counter()
    if k_serial:
        integrate((0, k_serial, k_serial))              # serial phase (constant work)
    parts = pool.map(integrate, [(i * k, k, n_total) for i in range(P)], chunksize=1)
    pi = float(sum(parts))
    return time.perf_counter() - t0, pi


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--threads", default=None, help="comma list, default: powers of two up to hardware threads")
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--k", type=int, default=30_000_000, help="intervals per worker (constant under weak scaling)")
    ap.add_argument("--serial-frac", type=float, default=0.0, help="injected serial fraction in [0,1)")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results.csv"))
    a = ap.parse_args()

    threads = [int(x) for x in a.threads.split(",")] if a.threads else default_thread_list()
    k_serial = int(round(a.serial_frac / (1.0 - a.serial_frac) * a.k)) if a.serial_frac > 0 else 0
    print(f"hardware threads: {hw_threads()}  | thread counts: {threads} | k={a.k} | runs={a.runs} | k_serial={k_serial}",
          file=sys.stderr)

    rows = []
    for P in threads:
        with mp.Pool(P) as pool:
            run_once(pool, P, min(a.k, 1_000_000), 0)       # pool warm-up (not recorded)
            run_once(pool, P, a.k, k_serial)                # one full warm-up run (not recorded)
            for r in range(1, a.runs + 1):
                t, pi = run_once(pool, P, a.k, k_serial)
                rows.append((P, r, a.k, a.serial_frac, t, pi))
                print(f"P={P:3d} run={r}  {t:8.4f}s  pi={pi:.12f}", file=sys.stderr)

    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["threads", "run", "k_per_worker", "serial_frac_injected", "wall_s", "pi_estimate"])
        for row in rows:
            w.writerow([row[0], row[1], row[2], row[3], f"{row[4]:.6f}", f"{row[5]:.12f}"])
    print("wrote", os.path.abspath(a.out), file=sys.stderr)


if __name__ == "__main__":
    main()
