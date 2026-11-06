#!/usr/bin/env python3
"""
Task 21 - Amdahl vs. Gustafson parametric simulator.

Models, for serial fraction f and P processors
    Amdahl     S_A(P) = 1 / (f + (1 - f) / P)          (strong scaling, fixed size)
    Gustafson  S_G(P) = P - f * (P - 1)                 (weak scaling, fixed time)
and the corresponding parallel efficiencies E = S / P.

Outputs
    <out>/speedup_table.csv      structured data (one row per (alpha, P))
    <out>/scaling_overlay.png/.pdf  overlay plots (needs matplotlib; skip with --no-plots)

Examples
    python simulator.py
    python simulator.py --alphas 0.001,0.01,0.05,0.2 --pmax 65536 --out ../plots
    python simulator.py --pmin 1 --pmax 1024 --alphas 0.04 --no-plots
"""
import argparse
import csv
import math
import os
import sys

P_LIMITS = (1, 65536)
ALPHA_LIMITS = (0.001, 0.20)
DEFAULT_ALPHAS = [0.001, 0.01, 0.04, 0.08, 0.20]


def amdahl(P: float, s: float) -> float:
    return 1.0 / (s + (1.0 - s) / P)


def gustafson(P: float, a: float) -> float:
    return P - a * (P - 1.0)


def core_counts(pmin: int, pmax: int):
    """Powers of two between pmin and pmax (inclusive), plus pmax itself."""
    out, p = [], 1
    while p < pmin:
        p *= 2
    while p <= pmax:
        out.append(p)
        p *= 2
    if pmin not in out:
        out.insert(0, pmin)
    if pmax not in out:
        out.append(pmax)
    return sorted(set(out))


def simulate(alphas, cores):
    rows = []
    for a in alphas:
        for P in cores:
            sa, sg = amdahl(P, a), gustafson(P, a)
            rows.append({
                "alpha": a, "P": P,
                "amdahl_speedup": sa, "gustafson_speedup": sg,
                "amdahl_efficiency": sa / P, "gustafson_efficiency": sg / P,
                "gustafson_over_amdahl": sg / sa,
                "amdahl_limit_1_over_s": 1.0 / a,
            })
    return rows


def write_csv(rows, path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.10g}" if isinstance(v, float) else v) for k, v in r.items()})


def make_plots(rows, alphas, cores, outdir):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed - skipping plots (pip install matplotlib)", file=sys.stderr)
        return
    cmap = plt.get_cmap("viridis")
    colors = {a: cmap(i / max(1, len(alphas) - 1) * 0.9) for i, a in enumerate(alphas)}
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
    ax[0].plot(cores, cores, "k:", lw=1.2, label="ideal  S = P")
    for a in alphas:
        sub = [r for r in rows if r["alpha"] == a]
        ax[0].plot(cores, [r["gustafson_speedup"] for r in sub], "-", color=colors[a], lw=2,
                   label=f"Gustafson  α={a:g}")
        ax[0].plot(cores, [r["amdahl_speedup"] for r in sub], "--", color=colors[a], lw=2,
                   label=f"Amdahl  s={a:g}")
    ax[0].set(xscale="log", yscale="log", xlabel="processors P", ylabel="speedup S(P)",
              title="Strong (Amdahl, dashed) vs weak (Gustafson, solid) scaling")
    ax[0].grid(True, which="both", alpha=0.3)
    ax[0].legend(fontsize=7, ncol=2)
    for a in alphas:
        sub = [r for r in rows if r["alpha"] == a]
        ax[1].plot(cores, [r["gustafson_efficiency"] for r in sub], "-", color=colors[a], lw=2)
        ax[1].plot(cores, [r["amdahl_efficiency"] for r in sub], "--", color=colors[a], lw=2)
    ax[1].set(xscale="log", yscale="log", xlabel="processors P", ylabel="efficiency S/P",
              title="Parallel efficiency (Gustafson → 1-α, Amdahl → 0)")
    ax[1].grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    os.makedirs(outdir, exist_ok=True)
    for ext in ("png", "pdf"):
        p = os.path.join(outdir, f"scaling_overlay.{ext}")
        fig.savefig(p, dpi=200)
        print("wrote", p)


def parse_floats(s):
    return [float(x) for x in s.split(",") if x.strip()]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pmin", type=int, default=1)
    ap.add_argument("--pmax", type=int, default=65536)
    ap.add_argument("--alphas", type=parse_floats, default=DEFAULT_ALPHAS,
                    help="comma-separated serial fractions in [0.001, 0.20]")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "plots"),
                    help="output directory (CSV + plots)")
    ap.add_argument("--csv", default=None, help="explicit CSV path (default: <out>/speedup_table.csv)")
    ap.add_argument("--no-plots", action="store_true")
    a = ap.parse_args(argv)

    if not (P_LIMITS[0] <= a.pmin <= a.pmax <= P_LIMITS[1]):
        ap.error(f"need {P_LIMITS[0]} <= pmin <= pmax <= {P_LIMITS[1]}")
    for x in a.alphas:
        if not (ALPHA_LIMITS[0] <= x <= ALPHA_LIMITS[1]):
            ap.error(f"alpha={x} outside [{ALPHA_LIMITS[0]}, {ALPHA_LIMITS[1]}]")

    cores = core_counts(a.pmin, a.pmax)
    rows = simulate(a.alphas, cores)
    csv_path = a.csv or os.path.join(a.out, "speedup_table.csv")
    write_csv(rows, csv_path)
    print(f"wrote {csv_path}  ({len(rows)} rows)")
    if not a.no_plots:
        make_plots(rows, a.alphas, cores, a.out)


if __name__ == "__main__":
    main()
