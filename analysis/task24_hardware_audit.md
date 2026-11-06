# Task 24 — Hardware Audit & Empirical-vs-Theoretical Discrepancy

> **TEMPLATE — fill in with *your* machine and *your* measurements.**
> The numbers below can only come from running `benchmarks/` on your hardware; nothing here is pre-filled on purpose.
> Generate the raw facts with `sh benchmarks/collect_hw_info.sh > analysis/hw_info.txt`.

## 1. Hardware description (fill from `hw_info.txt`)

| Item | Value |
|---|---|
| CPU model / microarchitecture | `[lscpu: Model name]` |
| Sockets × physical cores × SMT threads | `[ ]` × `[ ]` × `[ ]` = `[ ]` hardware threads |
| Base / all-core turbo / single-core turbo | `[ ]` / `[ ]` / `[ ]` GHz |
| L1d / L1i per core | `[ ]` KiB |
| L2 per core (or per cluster) | `[ ]` |
| L3 (shared? per CCX/socket) | `[ ]` MiB |
| Memory: channels × DIMM type/speed → peak BW | `[ ]` |
| NUMA nodes and distances | `[numactl --hardware]` |
| OS / kernel / governor | `[ ]` |
| Compiler / Python / NumPy versions | `[ ]` |

## 2. Results (from `benchmarks/fit_gustafson.py` — paste output)

| $P$ | mean $T$ [s] | std [s] | $S$ | $E$ |
|---:|---:|---:|---:|---:|
| `[ ]` | | | | |

$\alpha_{observed}=\ [\ ]\pm[\ ]$, $R^2=[\ ]$. Plot: `plots/scaling_comparison.pdf`.

## 3. Checklist of effects that make measurements deviate from $S=P-\alpha(P-1)$

| Effect | Signature in the data | How to check / control |
|---|---|---|
| **Turbo boost / frequency scaling** | $T_1$ was measured at a higher clock than $T_P$ → $S/P$ < 1 even if $\alpha=0$; smooth decline in $E$ | `grep MHz /proc/cpuinfo` during runs, `turbostat`; set governor `performance`, or fix frequency |
| **Thermal throttling / power capping** | Late runs and high-$P$ runs slower; large run-to-run std; $E$ drops at highest $P$ | `sensors`, `turbostat` (Tctl, PkgWatt), run order randomisation, cool-down pauses |
| **SMT (hyper-threads)** | For $P>$ physical cores, $S$ rises only ≈ 1.1–1.3× per added core pair; kink in the curve exactly at the physical-core count | repeat with threads ≤ physical cores; compare with `lscpu` topology |
| **NUMA boundaries** | Kink when threads spill to 2nd socket/CCD; remote memory accesses slower | `numactl --hardware`; pin threads (`OMP_PROC_BIND=close OMP_PLACES=cores`, `taskset`); first-touch initialisation |
| **Shared cache / memory bandwidth** | Cores contend for L3/DRAM; this benchmark is compute-bound so effect small — mention if you switch to a streaming kernel | `perf stat -e cache-misses`, STREAM benchmark for peak bandwidth |
| **Process start / IPC (Python only)** | Constant extra per-run cost raises $\alpha$ artificially | use the OpenMP version for comparison |
| **OS noise / other load** | outliers, high std | close other apps, use `nice`, repeat ≥ 5 runs, report SEM |
| **Wrong baseline** | $T_1$ not representative | always use the same code path & pool for $P=1$ (the harness does) |

## 4. Discussion prompts (answer with your data)

1. Where does the measured curve leave the Gustafson fit? Does that coincide with a hardware boundary (physical-core count, socket boundary)?
2. Is $\alpha_{observed}$ a *serial fraction* or a catch-all for frequency drop + SMT + overhead? (Compare with the `--serial-frac` injection run: the fit should recover the injected value on a machine without those effects.)
3. Compute the Amdahl curve with the same $\alpha$: why does it look pessimistic here (Task 03)?
4. Which single change (pinning, governor, fewer threads, larger $k$) most improved agreement?
