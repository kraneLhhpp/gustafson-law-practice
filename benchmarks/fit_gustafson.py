#!/usr/bin/env python3
"""
Task 23 - Statistics + least-squares extraction of the empirical serial fraction.

Input : results.csv (columns threads,run,k_per_worker,serial_frac_injected,wall_s,...)  - from either benchmark.
Method: weak-scaling ("scaled") speedup of every run
            S_run(P) = P * T1 / T_run(P),     T1 = mean wall time at P = 1
        Gustafson:  S(P) = P - alpha*(P-1)   <=>   y = alpha * x   with  y = P - S,  x = P - 1  (line through the origin)
        OLS:        alpha = sum(x*y) / sum(x^2),   se(alpha) = sqrt( sum((y-alpha*x)^2)/(n-1) / sum(x^2) )
        (Also reports an unconstrained fit S = a + b*P as a diagnostic: b should be ~ 1-alpha, a ~ alpha.)

Outputs: summary.csv (mean, std, sem, S, E per thread count) and fit_results.json  (used by ../plots/make_plots.py).

Usage:  python3 fit_gustafson.py [--csv results.csv] [--outdir .]
"""
import argparse
import csv
import json
import math
import os
from collections import defaultdict

import numpy as np


def load(path):
    data, injected = defaultdict(list), set()
    with open(path) as fh:
        for r in csv.DictReader(fh):
            data[int(r["threads"])].append(float(r["wall_s"]))
            if "serial_frac_injected" in r:
                injected.add(float(r["serial_frac_injected"]))
    return data, injected


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", default=os.path.join(here, "results.csv"))
    ap.add_argument("--outdir", default=here)
    a = ap.parse_args()

    data, injected = load(a.csv)
    if 1 not in data:
        raise SystemExit("results.csv must contain P=1 runs (the weak-scaling baseline T1).")
    Ps = sorted(data)
    if len(Ps) < 5:
        print(f"warning: only {len(Ps)} thread counts; Task 23 asks for at least 5")
    t1 = np.array(data[1])
    T1, T1_sem = t1.mean(), (t1.std(ddof=1) / math.sqrt(len(t1)) if len(t1) > 1 else 0.0)

    summary, xs, ys, Ss, Pall = [], [], [], [], []
    for P in Ps:
        t = np.array(data[P])
        mean, std = t.mean(), (t.std(ddof=1) if len(t) > 1 else 0.0)
        sem = std / math.sqrt(len(t)) if len(t) > 1 else 0.0
        S = P * T1 / mean
        S_err = S * math.sqrt((sem / mean) ** 2 + (T1_sem / T1) ** 2)
        summary.append(dict(threads=P, n_runs=len(t), mean_s=mean, std_s=std, sem_s=sem, S=S, S_err=S_err,
                            E=S / P, E_err=S_err / P))
        for tr in t:                                    # regression uses every individual run
            S_run = P * T1 / tr
            xs.append(P - 1.0); ys.append(P - S_run); Ss.append(S_run); Pall.append(P)

    x, y = np.array(xs), np.array(ys)
    alpha = float((x * y).sum() / (x * x).sum())
    resid = y - alpha * x
    se = float(math.sqrt((resid ** 2).sum() / max(1, len(x) - 1) / (x * x).sum()))
    S_arr, P_arr = np.array(Ss), np.array(Pall)
    ss_res = float(((S_arr - (P_arr - alpha * (P_arr - 1))) ** 2).sum())
    ss_tot = float(((S_arr - S_arr.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    b, a0 = np.polyfit(P_arr, S_arr, 1)                 # diagnostic S = a0 + b*P

    result = dict(alpha_observed=alpha, alpha_stderr=se, r_squared=r2, T1_mean_s=T1,
                  diagnostic_slope_b=float(b), diagnostic_intercept_a=float(a0),
                  implied_alpha_from_slope=float(1 - b), n_points=int(len(x)),
                  injected_serial_fraction=sorted(injected))
    os.makedirs(a.outdir, exist_ok=True)
    with open(os.path.join(a.outdir, "fit_results.json"), "w") as fh:
        json.dump(result, fh, indent=2)
    with open(os.path.join(a.outdir, "summary.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(summary[0].keys()))
        w.writeheader()
        for r in summary:
            w.writerow({k: (f"{v:.6g}" if isinstance(v, float) else v) for k, v in r.items()})

    print(f"{'P':>4} {'runs':>4} {'mean[s]':>9} {'std[s]':>8} {'S':>8} {'E':>7}")
    for r in summary:
        print(f"{r['threads']:>4} {r['n_runs']:>4} {r['mean_s']:>9.4f} {r['std_s']:>8.4f} {r['S']:>8.3f} {r['E']:>7.3f}")
    print(f"\nalpha_observed = {alpha:.5f} ± {se:.5f}   (R^2 on S = {r2:.4f}, n = {len(x)})")
    print(f"diagnostic S = {a0:.3f} + {b:.4f} P  -> alpha from slope = {1 - b:.5f}")
    if injected and injected != {0.0}:
        print(f"injected serial fraction = {sorted(injected)}  (compare with alpha_observed)")


if __name__ == "__main__":
    main()
