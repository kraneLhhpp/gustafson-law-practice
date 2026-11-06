# Task 11 — Gustafson vs. Sun–Ni Memory-Bounded Speedup

## 1. Models

Let $s$ = serial fraction of the **base** (1-processor) problem, and $G(P)$ = factor by which the *parallel* workload
grows when the memory available grows $P$-fold ($G$ is determined by the algorithm: if work $\sim n^{a}$ and memory $\sim n^{b}$ then $G(P)=P^{a/b}$).

$$\boxed{S^{*}(P)=\frac{s+(1-s)\,G(P)}{s+(1-s)\,G(P)/P}}\qquad(\text{Sun–Ni})$$

| $G(P)$ | Result | Model |
|---|---|---|
| $1$ | $\dfrac{1}{s+(1-s)/P}$ | Amdahl (fixed-size) |
| $P$ | $\dfrac{s+(1-s)P}{1}=s+(1-s)P$ | **Gustafson** (fixed-time) |
| $G>P$ | between Gustafson and $P$ | memory-bounded, work grows super-linearly |
| $G<P$ | between Amdahl and Gustafson | memory-bounded, work grows sub-linearly |

(With $G=P$ the denominator is $s+(1-s)=1$, so Sun–Ni collapses to Gustafson's formula exactly.)

## 2. Numerical comparison ($s=0.04$, $P=64$)

| $G(P)$ | $S^*$ |
|---|---:|
| $1$ (Amdahl) | 18.18 |
| $P^{2/3}=16$ | 55.00 |
| $P=64$ (Gustafson) | 61.48 |
| $P^{3/2}=512$ (dense GEMM: work $N^3$, memory $N^2$) | 63.67 |

Note $S^*\le P$ always: as $G\to\infty$, $S^*\to P$.

## 3. Conditions where Gustafson is wrong

**Gustafson over-estimates** ($G_{real}<P$) when the problem **cannot grow linearly in work**:

* each node must hold *replicated* data (lookup tables, a global mesh description, a full vector in an all-gather
  formulation) that grows with $n$ → usable per-node memory for distributed data shrinks;
* the algorithm needs *superlinear memory per unit work* (data-heavy analytics, large halo/overlap, graph frontiers);
* the machine's memory per core shrinks with $P$ (many-core nodes) while the fixed-time model assumes constant memory per core.

Then the memory wall stops you from filling the time budget, and real speedup is lower. (It also over-estimates whenever overheads grow with
$P$ — Task 12.)

**Gustafson under-estimates** the *speedup ratio* ($G_{real}>P$) when work grows faster than memory
($a>b$: dense GEMM $P^{3/2}$, direct N-body $P^{2}$, dense LU $P^{3/2}$): the memory-filling problem has an even smaller effective serial fraction.
**But** such a problem runs *longer*, $T\propto G/P$; Gustafson's fixed-time premise is violated — the model is not wrong, it answers a different question.

**They coincide** when $a=b$ (stencils, sparse mat-vec, Monte Carlo with state ∝ samples): the memory-limit problem and the time-limit problem are the same size.

## 4. Take-away

Gustafson = Sun–Ni with the *specific* choice $G=P$. Before using it, ask which resource binds first —
time (Gustafson), memory (Sun–Ni), or neither (Amdahl).
