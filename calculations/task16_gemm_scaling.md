# Task 16 — Dense GEMM ($C=A\times B$) under Gustafson Scaling

## Derivation

Work $W(N)=2N^3$ flops $\propto N^3$; memory $\propto N^2$. Ideal parallel time $T(P)=\dfrac{c\,N^3}{P}$.
Gustafson (fixed time): $T(P)=T(1)$ for the *base* problem $N_1$:

$$\frac{c\,N(P)^3}{P}=c\,N_1^3\;\Longrightarrow\;\boxed{N(P)=N_1\,P^{1/3}}$$

(equivalently $W(P)=P\,W(1)$, Task 10). Doubling the processor count increases $N$ only by $2^{1/3}=1.26$; $\times8$ processors → $\times2$ dimension.

## Scaling targets ($N_1=2048$; 3 matrices of doubles)

| $P$ | $N(P)=2048P^{1/3}$ | $N/N_1$ | memory/node (MB) | Sun–Ni size $N_1\sqrt P$ |
|---:|---:|---:|---:|---:|
| 1 | 2 048 | 1.00 | 100.7 | 2 048 |
| 8 | 4 096 | 2.00 | 50.3 | 5 793 |
| 16 | 5 161 | 2.52 | 39.9 | 8 192 |
| 64 | 8 192 | 4.00 | 25.2 | 16 384 |
| 128 | 10 321 | 5.04 | 20.0 | 23 170 |
| 512 | 16 384 | 8.00 | 12.6 | 46 341 |
| 1 024 | 20 643 | 10.08 | 10.0 | 65 536 |
| 4 096 | 32 768 | 16.00 | 6.3 | 131 072 |
| 32 768 | 65 536 | 32.00 | 3.1 | 370 728 |

## Consequences

1. **Memory per node *shrinks*** as $P^{-1/3}$ (total memory $\propto N^2=P^{2/3}$ grows slower than $P$): fixed-time GEMM *under-uses* memory.
   The memory-bounded alternative (fill memory: $N\propto\sqrt P$, Sun–Ni, Task 11) has work $\propto P^{3/2}$ and time $\propto\sqrt P$.
2. **Communication.** With a 2-D algorithm (Cannon/SUMMA) each rank moves $\Theta(N^2/\sqrt P)=\Theta(P^{2/3-1/2})=\Theta(P^{1/6})$ words
   while per-rank flops stay constant ⇒ comm/compute ratio grows as $P^{1/6}$ (×2 at $P=64$, ×4 at $P=4096$) — mild, but it means
   $\alpha_{eff}$ creeps upward (Task 12). A 3-D/2.5-D algorithm trades memory for lower communication.
3. GEMM is the "friendly" case: regular, compute-bound ($O(N)$ flops per word moved) — a good model of Gustafson behaviour.
