# Task 06 — Parametric Speedup ($\alpha = 0.04$)

Formulas: $S(P)=P-\alpha(P-1)$, $E(P)=S(P)/P$, lost cores $=P-S=\alpha(P-1)$.

| $P$ | $\alpha(P-1)$ | $S(P)$ | $E(P)$ |
|---:|---:|---:|---:|
| 16 | 0.60 | 15.40 | 0.962 500 |
| 64 | 2.52 | 61.48 | 0.960 625 |
| 256 | 10.20 | 245.80 | 0.960 156 |
| 1 024 | 40.92 | 983.08 | 0.960 039 |
| 4 096 | 163.80 | 3 932.20 | 0.960 010 |
| 16 384 | 655.32 | 15 728.68 | 0.960 002 |

Example (P = 1024): $S=1024-0.04\cdot1023=1024-40.92=983.08$; $E=983.08/1024=0.960039$.

## Evaluation

* **Efficiency does *not* degrade meaningfully** as $P$ grows exponentially: it falls from 96.25 % to 96.0002 %.
  The drop is exactly $\alpha/P$ above the asymptote $1-\alpha=0.96$ (Task 04): 0.0025 at $P=16$, 0.0000024 at $P=16384$.
* What *does* grow is the **absolute number of "wasted" cores**: $\alpha(P-1)$ goes from 0.6 to 655 — 4 % of the machine
  is always idle, and 4 % of a big machine is a lot of cores. So $E$ is flat but the *cost* of the serial part in
  absolute core-hours scales linearly with $P$.
* Caveat: this assumes α is constant. If α grows with $P$ (communication, Task 12) efficiency does degrade.
