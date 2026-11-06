# Task 05 — Case Reconstruction: the 1024-processor nCUBE and "Amdahl's Pessimism"

*Sources: J. L. Gustafson, G. R. Montry, R. E. Benner, "Development of Parallel Methods for a 1024-Processor
Hypercube", SIAM J. Sci. Stat. Comput. 9(4), 609–638 (1988); J. L. Gustafson, "Reevaluating Amdahl's Law",
Commun. ACM 31(5), 532–533 (1988). Figures below were checked against these two papers.*

## 1. Scenario

Sandia National Laboratories, 1988. A 1024-node nCUBE hypercube (MIMD, message passing).
Three production applications were parallelised:

| Application | Method | Scaled speedup (CACM) |
|---|---|---:|
| Beam stress analysis | conjugate gradients | 1021 |
| Baffled surface-wave simulation | explicit finite differences | 1020 |
| Unstable fluid flow | flux-corrected transport | 1016 |

The SIAM paper's abstract gives the range **1009–1020** for scaled problems (slightly different from the
CACM figure of 1021 for the beam problem — quote "≈1000–1020" if you need one safe statement) and
**502–637** when the problem size was held *fixed*.

## 2. Why this "contradicted" Amdahl

* Measured serial fraction *on the parallel machine*: $s'=0.4$–$0.8\%$.
* Reading that as Amdahl's $s$: bound $1/s=125$–$250$; at $P=1024$,
  $S_A=1/(0.004+0.996/1024)\approx201$ (and $\approx111$ for $s=0.008$).
  Observed: $\approx1000$. A factor of 5–9 beyond "impossible".

## 3. How problem expansion dismantles the ceiling

1. The runs were **scaled**: the per-processor sub-problem was kept constant, so the global problem grew ≈1024×
   (more grid points / finite elements).
2. The serial work (set-up, I/O of small inputs, global control) did **not** grow with it. Hence its fraction of a
   *single-processor* run of the scaled problem was only
   $$s_1=\frac{s'}{s'+(1-s')\,1024}\approx\frac{0.004}{1020}\approx4\times10^{-6}\quad(\text{to }8\times10^{-6}\text{ for }0.8\%)$$
   — the "3–10 parts per million" quoted in the SIAM abstract.
3. Amdahl with *that* $s_1$: $1/(4\times10^{-6}+1/1024)\approx1020$ ✔. The ceiling $1/s_1\approx2.5\times10^5$ is far away.
4. The fixed-size runs (502–637×) show the other side: at fixed problem size the per-processor
   work shrinks 1024× and communication/serial overheads bite — exactly Amdahl's regime.

## 4. Methodological consequence — measuring scaled speedup

A scaled problem generally cannot be run on a single node, so scaled speedup is **computed from the $P$-node run**
as $S=s'+pP$ (CACM Fig. 2b). With a constant per-processor sub-problem this is equivalent to
$P\cdot T_{1}(\text{per-node size})/T_P(P\times\text{ size})$ — the quantity
`benchmarks/weak_scale_bench` measures (Tasks 22–23).

## 5. Take-away

"Amdahl's pessimism" is not a flaw in Amdahl's algebra, but an **unstated assumption** (fixed $n$, hence a
fixed serial *fraction*). Where the problem can grow, the serial fraction shrinks as $\propto1/P$ and the
ceiling moves away. Equally, Gustafson's result is not a law that "always" gives linear speedup: it requires that
serial *time* stay constant and per-processor overhead stay negligible.
