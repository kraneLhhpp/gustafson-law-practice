# Task 17 — 7-Point 3-D Stencil: Surface-to-Volume under Weak Scaling

## Setup

Global cube $N^3$ split into $P$ equal sub-cubes of edge $n$ ($N=nP^{1/3}$, $n^3=N^3/P$).
Per time step each rank: computes $\approx 8\,n^3$ flops ($c_f n^3$) and exchanges 6 faces ($\approx6n^2$ words) with neighbours.

## Weak scaling (Gustafson): $N^3=P\,N_1^3$ ⇒ $n=N_1$ constant

$$\frac{\text{comm}}{\text{comp}}\Big|_{\text{per rank}}=\frac{6n^2\,t_w}{c_fn^3t_f}=\frac{6\,t_w}{c_f\,t_f}\cdot\frac{1}{n}=\frac{6}{n}\cdot\text{const}\;=\;\text{constant in }P.$$

* Per-rank communication volume $=\Theta(N_1^2)$: **constant**, because every halo exchange is with ≤6 neighbours.
* Per-rank compute $=\Theta(N_1^3)$: constant. ⇒ $T_{step}(P)\approx\text{const}$ ⇒ α does not grow ⇒ **ideal Gustafson behaviour**.
* *Global* surface-to-volume ratio of the whole domain $\sim N^2/N^3=1/N\propto P^{-1/3}$ improves, but that is irrelevant: what limits scaling is the
  **per-rank** ratio $6/n$, which is fixed by the chosen grain.

## Contrast: strong scaling (fixed $N$)

$n=N/P^{1/3}$ ⇒ $\dfrac{\text{comm}}{\text{comp}}=\dfrac{6}{n}=\dfrac{6P^{1/3}}{N}$ — **degrades** as $P^{1/3}$; Amdahl-type behaviour.

| $P$ | $n$ (weak, $N_1=256$) | $6/n$ | $n$ (strong, $N=1024$) | $6/n$ |
|---:|---:|---:|---:|---:|
| 1 | 256 | 0.0234 | 1024 | 0.0059 |
| 8 | 256 | 0.0234 | 512 | 0.0117 |
| 64 | 256 | 0.0234 | 256 | 0.0234 |
| 512 | 256 | 0.0234 | 128 | 0.0469 |
| 4 096 | 256 | 0.0234 | 64 | 0.0938 |

## Caveats (what keeps α non-zero)

* Nearest-neighbour latency per message and imperfect overlap — constant per step, so a constant fraction.
* Global operations (residual norm, `Allreduce`, time-step control): $\Theta(\log P)$, slowly growing α.
* Explicit schemes: CFL condition makes $\Delta t\propto\Delta x$ so the *number of steps* needed for fixed simulated time grows as $P^{1/3}$ (Task 13).
* Memory-bandwidth saturation within a node (stencils are bandwidth-bound) dominates real measurements.
