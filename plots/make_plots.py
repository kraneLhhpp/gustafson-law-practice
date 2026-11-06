#!/usr/bin/env python3
"""
Task 24 - publication-quality plots: ideal vs Gustafson fit vs measured (SEM error bars) vs Amdahl (same fraction).

Usage: python3 make_plots.py [--bench-dir DIR] [--out-dir DIR]
Needs benchmarks/summary.csv and benchmarks/fit_results.json (run benchmarks/fit_gustafson.py first).
Writes plots/scaling_comparison.pdf (vector) and .png (300 dpi).
"""
import csv
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--bench-dir", default=os.path.join(HERE, "..", "benchmarks"),
                help="directory holding summary.csv and fit_results.json")
ap.add_argument("--out-dir", default=HERE)
args = ap.parse_args()
BENCH = args.bench_dir

with open(os.path.join(BENCH, "fit_results.json")) as fh:
    fit = json.load(fh)
rows = list(csv.DictReader(open(os.path.join(BENCH, "summary.csv"))))
P = np.array([int(r["threads"]) for r in rows])
S = np.array([float(r["S"]) for r in rows])
Se = np.array([float(r["S_err"]) for r in rows])
alpha = fit["alpha_observed"]

grid = np.linspace(1, P.max(), 400)
plt.rcParams.update({"font.size": 11, "axes.grid": True, "grid.alpha": 0.3})
fig, ax = plt.subplots(figsize=(6.4, 4.8))
ax.plot(grid, grid, "k:", lw=1.3, label="ideal linear  $S=P$")
ax.plot(grid, grid - alpha * (grid - 1), "-", lw=2, color="tab:blue",
        label=fr"Gustafson fit  $\alpha={alpha:.4f}\pm{fit['alpha_stderr']:.4f}$")
ax.plot(grid, 1.0 / (alpha + (1 - alpha) / grid), "--", lw=2, color="tab:red",
        label=fr"Amdahl, same fraction  ($S_\infty={1/alpha:.1f}$)" if alpha > 0 else "Amdahl")
ax.errorbar(P, S, yerr=Se, fmt="o", ms=6, capsize=4, color="tab:green", label="measured (mean ± SEM)")
ax.set(xlabel="threads $P$ (work per thread constant)", ylabel="scaled speedup $S(P)=P\\,T_1/T_P$",
       title="Weak scaling: measurement vs. Gustafson and Amdahl")
ax.legend(fontsize=9, loc="upper left")
fig.tight_layout()
os.makedirs(args.out_dir, exist_ok=True)
for ext, kw in (("pdf", {}), ("png", {"dpi": 300})):
    out = os.path.join(args.out_dir, f"scaling_comparison.{ext}")
    fig.savefig(out, **kw)
    print("wrote", out)
