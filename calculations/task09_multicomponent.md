# Task 09 — Multi-Component Workload

Phases (fractions of the **parallel** execution time, so they are Gustafson-style fractions):

| Phase | Description | Share | Treated as |
|---|---|---:|---|
| A | initial disk I/O + parameter broadcast | 2 % | serial |
| B | boundary message-passing synchronisation | 6 % | serial (as stated in the task) |
| C | core domain flux computation | 92 % | parallel |

**Aggregate serial fraction:** $\alpha=0.02+0.06=\mathbf{0.08}$, $p=0.92$.

**Scaled speedup** $S=P-\alpha(P-1)$:

| $P$ | $\alpha(P-1)$ | $S(P)$ | $E(P)$ |
|---:|---:|---:|---:|
| 512 | 40.88 | **471.12** | 0.9202 |
| 2 048 | 163.76 | **1 884.24** | 0.9200 |

Cross-check via $S=s+pP$: $0.08+0.92\cdot512=471.12$ ✔; $0.08+0.92\cdot2048=1884.24$ ✔.

## Remarks

* Treating B as **serial** is a modelling choice made by the exercise. In reality halo-exchange is performed *concurrently* by all ranks
  and its cost per rank is roughly independent of $P$ (Task 17), i.e. it is a **per-processor overhead inside the parallel time**,
  not a serial section. If only A were serial ($\alpha=0.02$): $S(512)=501.78$, $S(2048)=2007.06$.
  Be explicit in a report about which interpretation you use.
* Phase A is the true Gustafson-style serial part; if its time grows with $P$ (broadcast $\propto\log P$, parallel I/O contention)
  $\alpha$ grows with $P$ and these numbers become optimistic (Task 12).
