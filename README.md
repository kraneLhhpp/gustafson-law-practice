# Gustafson's Law & Weak Scaling — Practice Repository

*Parallel & Distributed Computing Architecture — ungraded comprehensive practice (instructor: Sufyan bin Uzayr).*
All work lives in `gustafson-law-practice/`: `theory/`, `calculations/`, `benchmarks/`, `analysis/`, `plots/`.

## Table of contents

1. [Core rules at a glance](#1-core-rules-at-a-glance)
2. [When to design around Gustafson weak scaling](#2-when-to-design-around-gustafson-weak-scaling)
3. [Architectural synthesis (Tasks 01–24)](#3-architectural-synthesis-tasks-0124)
4. [Artifact index](#4-artifact-index)
5. [Execution commands](#5-execution-commands)
6. [Status: what you still have to produce on your own machine](#6-status)
7. [Sources](#7-sources)

## 1. Core rules at a glance

| Quantity | Formula | Remarks |
|---|---|---|
| Amdahl (fixed size) | $S_A=\dfrac{1}{s+(1-s)/P}\to\dfrac1s$ | $s$ measured on 1 processor; $E_A\to0$ |
| **Gustafson (fixed time)** | $S=P-\alpha(P-1)=s+pP$ | $\alpha$ measured on the **$P$-processor run** |
| Efficiency | $E=1-\alpha+\alpha/P\to1-\alpha$ | plateau, never → 0 (Task 04) |
| Equivalence | $s_1=\dfrac{\alpha}{\alpha+(1-\alpha)P}$ turns Amdahl into Gustafson | one law, two frames (Task 03) |
| Tolerable α | $\alpha_{max}=\dfrac{P-S_{req}}{P-1}$ | e.g. $P=8192,S\ge7500\Rightarrow\alpha\le8.45\%$ (Task 07) |
| With comm. penalty | $S_c=\dfrac{P-\alpha(P-1)}{1+c(P)}$ | $c\sim\log P$ or $\sqrt P$ ⇒ no plateau (Task 12) |
| Memory-bounded (Sun–Ni) | $S^*=\dfrac{s+(1-s)G(P)}{s+(1-s)G(P)/P}$ | $G=1$ Amdahl, $G=P$ Gustafson (Task 11) |
| Isoefficiency | $T_o=s(P-1)\Rightarrow W=\Theta(P)$ | Gustafson scaling is the optimal isoefficiency (Task 14) |
| Energy | $E_P-E_1'=P_{idle}\,T\,\alpha(P-1)$ | parallelism buys time, not joules (Task 15) |

## 2. When to design around Gustafson weak scaling

**Do** (the premises hold) when:

* the problem has a *resolution knob* (grid points, particles, samples, ensemble members) and science improves with size;
* serial **time** is constant (input parsing, set-up) and does not grow with the problem;
* communication per rank is constant (nearest-neighbour halo exchange, Task 17) or hideable; global operations are $O(\log P)$ and tiny;
* memory per node is the natural limiter and work ∝ memory (stencils, sparse mat-vec, Monte Carlo, Task 10/16/19).

**Don't** — use strong scaling/Amdahl, or Sun–Ni/isoefficiency, when:

* the deadline is for a **fixed** problem (latency-bound services, real-time control, a single query);
* complexity changes with size (CG iterations ∝ N, CFL time-steps, FFT/all-to-all, direct N-body — Tasks 13, 18);
* irregular access / skew (graph analytics, Task 20);
* serial work grows with the data (serial I/O of the whole mesh).

**Practical checklist:** (1) always state *what is held constant* when quoting speedup or efficiency; (2) measure α **on the parallel run**;
(3) fit α at several $P$ — if it grows with $P$ you have a communication/imbalance term, not a serial fraction (Task 12); (4) report mean ± SEM of ≥5 runs;
(5) control frequency, SMT, NUMA, pinning (Task 24); (6) reduce α first by removing serial I/O, flat collectives and imbalance (Task 19).

## 3. Architectural synthesis (Tasks 01–24)

* **Foundations (01–05).** Amdahl asks "how fast for this problem", Gustafson "how big in this time". They are algebraically equivalent
  (Task 03); the 1988 nCUBE results (≈1000× on 1024 nodes with $s'=0.4$–$0.8\%$) are explained by the serial fraction of the *scaled single-processor run* being only parts-per-million.
* **Numbers (06–10).** With 4 % serial time, efficiency is flat at 96 % from $P=16$ to 16 384 — the cost is 655 idle cores, not lower efficiency. A target $S\ge7500$ on 8192 cores tolerates α ≤ 8.45 %.
  The "same α in both laws" comparison gives a 927 % gap at $P=128$ — a frame-of-reference error, not a modelling disagreement. $N$ grows only as $P^{1/3}$ in 3-D.
* **Limits of the model (11–15).** Sun–Ni generalises via $G(P)$; any growing communication term destroys the plateau; Gustafson scaling is isoefficient only when overhead is $O(P)$; static power makes the serial phase cost energy.
* **Workloads (16–20).** GEMM ($N\propto P^{1/3}$, comm/compute $\propto P^{1/6}$), stencils (per-rank surface/volume constant — ideal), N-body (direct: $N\propto\sqrt P$ and $\sqrt P$ comm; Barnes–Hut: $N\propto P/\log P$),
  Monte Carlo (α dominated by I/O, flat reductions and stragglers — *not* tree reductions), graphs (α_eff grows).
* **Experiments (21–24).** Simulator for both laws; weak-scaling harness (Python + OpenMP) with a validated least-squares fit through the origin; plots with Amdahl at the same α; hardware-audit checklist.

## 4. Artifact index

| Task | Artifact | Type |
|---|---|---|
| 01 | [`theory/task01_scaling_models.md`](theory/task01_scaling_models.md) | analysis |
| 02 | [`theory/task02_derivation.md`](theory/task02_derivation.md) | derivation |
| 03 | [`theory/task03_serial_invariance.md`](theory/task03_serial_invariance.md) | memo |
| 04 | [`theory/task04_asymptotic_limits.md`](theory/task04_asymptotic_limits.md) | proofs |
| 05 | [`theory/task05_historical_ncube.md`](theory/task05_historical_ncube.md) | case study |
| 06 | [`calculations/task06_parametric_table.md`](calculations/task06_parametric_table.md) | numeric table |
| 07 | [`calculations/task07_tolerable_serial.md`](calculations/task07_tolerable_serial.md) | algebra |
| 08 | [`calculations/task08_cross_divergence.md`](calculations/task08_cross_divergence.md) | comparison |
| 09 | [`calculations/task09_multicomponent.md`](calculations/task09_multicomponent.md) | calculation |
| 10 | [`calculations/task10_memory_growth.md`](calculations/task10_memory_growth.md) | calculation |
| 06–10, 16–17 | [`calculations/verify_calculations.py`](calculations/verify_calculations.py), [`numeric_log.txt`](calculations/numeric_log.txt) | script + log |
| 11 | [`theory/task11_sun_ni_comparison.md`](theory/task11_sun_ni_comparison.md) | essay |
| 12 | [`theory/task12_communication_penalty.md`](theory/task12_communication_penalty.md) | model extension |
| 13 | [`theory/task13_failure_cases.md`](theory/task13_failure_cases.md) | failure analysis |
| 14 | [`theory/task14_isoefficiency.md`](theory/task14_isoefficiency.md) | proof |
| 15 | [`theory/task15_energy_scaling.md`](theory/task15_energy_scaling.md) | equations |
| 16 | [`calculations/task16_gemm_scaling.md`](calculations/task16_gemm_scaling.md) | proof + table |
| 17 | [`calculations/task17_stencil_scaling.md`](calculations/task17_stencil_scaling.md) | proof |
| 18 | [`analysis/task18_nbody_scaling.md`](analysis/task18_nbody_scaling.md) | write-up |
| 19 | [`analysis/task19_monte_carlo.md`](analysis/task19_monte_carlo.md) | analysis |
| 20 | [`analysis/task20_graph_processing.md`](analysis/task20_graph_processing.md) | essay |
| 21 | [`benchmarks/simulator.py`](benchmarks/simulator.py) | code (+CSV, plots) |
| 22 | [`benchmarks/weak_scale_bench/`](benchmarks/weak_scale_bench/) | code + README |
| 23 | [`benchmarks/fit_gustafson.py`](benchmarks/fit_gustafson.py), `benchmarks/results.csv` (**you generate**) | code + data |
| 24 | [`plots/make_plots.py`](plots/make_plots.py), `plots/scaling_comparison.{pdf,png}` (**you generate**), [`analysis/task24_hardware_audit.md`](analysis/task24_hardware_audit.md) (**you fill in**) | plots + audit |
| 25 | this `README.md` | documentation |

## 5. Execution commands

```bash
python3 -m pip install numpy matplotlib

# Tasks 06–10, 16–17: reproduce all numbers
python3 calculations/verify_calculations.py | tee calculations/numeric_log.txt

# Task 21: simulator -> plots/speedup_table.csv, plots/scaling_overlay.{png,pdf}
python3 benchmarks/simulator.py --alphas 0.001,0.01,0.04,0.08,0.20 --pmax 65536

# Task 22–23: benchmark on YOUR machine (see benchmarks/weak_scale_bench/README.md for the OpenMP variant)
cd benchmarks
python3 weak_scale_bench/weak_scale_bench.py --runs 5 --out results.csv
python3 fit_gustafson.py                 # alpha_observed ± se, summary.csv

# Task 24
sh collect_hw_info.sh > ../analysis/hw_info.txt
cd ../plots && python3 make_plots.py
```

## 6. Status

Everything in `theory/`, `calculations/`, `analysis/task18–20`, the simulator, the benchmark harnesses and the fitting/plotting scripts is complete and was
smoke-tested (the fit was validated on synthetic data with known α = 0.037 and recovered 0.0378 ± 0.0004).
What cannot be pre-made, because it depends on your hardware: **`benchmarks/results.csv`, `plots/scaling_comparison.*` and the filled-in `analysis/task24_hardware_audit.md`**.
Please read the derivations, re-run the scripts and adapt the text to your own wording before submitting.

## 7. Sources

* G. M. Amdahl, "Validity of the single processor approach to achieving large scale computing capabilities", AFIPS 1967.
* J. L. Gustafson, "Reevaluating Amdahl's Law", *Commun. ACM* 31(5), 1988.
* J. L. Gustafson, G. R. Montry, R. E. Benner, "Development of parallel methods for a 1024-processor hypercube", *SIAM J. Sci. Stat. Comput.* 9(4), 1988.
* X.-H. Sun, L. Ni, "Scalable problems and memory-bounded speedup", *JPDC* 19, 1993.
* A. Grama, A. Gupta, V. Kumar, "Isoefficiency: measuring the scalability of parallel algorithms and architectures", *IEEE Parallel & Distributed Technology*, 1993.
* Y. Shi, "Reevaluating Amdahl's Law and Gustafson's Law", Temple University (equivalence of the two laws).
