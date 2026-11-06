# Task 13 — When Gustafson's Weak-Scaling Premise Fails

Gustafson's law needs three things: (i) per-processor work can be held constant by growing the problem, (ii) the
parallel time then stays constant, (iii) serial *time* does not grow. Two classic algorithms break (ii)/(iii).

---

## Case A — Conjugate Gradient (CG) on an elliptic problem (3-D Poisson, unpreconditioned)

**Weak-scaling set-up.** Keep $n_{loc}^3$ unknowns per processor; global grid $N=n_{loc}P^{1/3}$ per dimension.

**Why constant time fails (algorithmic complexity changes with problem size).**

1. Cost per iteration: SpMV (nearest-neighbour halo, constant per rank) + 2 dot products (global `Allreduce`, $\Theta(\log P)$ latency).
2. Number of iterations: condition number $\kappa(A)=O(N^2)$ ⇒ iterations $\sim\sqrt\kappa=O(N)=O(P^{1/3})$.
3. Hence $T(P)\approx\underbrace{O(P^{1/3})}_{\text{iterations}}\times\bigl[t_{comp}+t_{halo}+O(\log P)\bigr]$ — **runtime grows with $P$** even though work per
   processor *per iteration* is constant. Total work $W\propto N^3\cdot N=N^4=P^{4/3}$, not $P$.

**Consequence.** Measured $S=P\,T(1)/T(P)$ falls like $P^{2/3}/\log P$ with no "serial fraction" in sight: $\alpha$ regression becomes meaningless
(fitted α drifts upward with $P$). Remedies: multigrid or good preconditioner (iterations $O(1)$, but coarse-grid communication appears), or define the
experiment per iteration rather than per solve.

*(Related: explicit time-stepping obeys a CFL limit $\Delta t\propto\Delta x$; refining the mesh $P^{1/3}$-fold requires $P^{1/3}$ more steps for the same simulated time, again breaking fixed-time.)*

---

## Case B — 3-D FFT (pencil/slab decomposition) / all-to-all transposes

**Weak-scaling set-up.** $N^3=P\,n_{loc}^3$ points, constant per rank.

**Why constant time fails.**

1. Compute: $O(N^3\log N)$ total ⇒ per rank $O(n_{loc}^3\log N)$ — **log factor grows** (mild).
2. Communication: each transpose is an all-to-all; every rank sends/receives $O(n_{loc}^3)$ data (constant per rank), but the total volume
   $\Theta(N^3)=\Theta(P)$ must cross the network **bisection**, whose bandwidth on a 3-D torus is only $\Theta(P^{2/3})$.
   ⇒ $t_{comm}\propto P/P^{2/3}=P^{1/3}$ (on a fat-tree with full bisection the growth is milder but latency/contention still increase).
3. The communication part is *not* a constant serial fraction $\alpha$ — it grows with $P$ — and it also does not overlap easily (global dependence).

**Consequence.** $T(P)=t_{comp}(1+\epsilon\log P)+\gamma P^{1/3}$ ⇒ efficiency decays polynomially. Gustafson's formula with constant α over-predicts.

---

## Summary table

| | CG | 3-D FFT |
|---|---|---|
| Premise broken | iteration count ∝ $N$ (algorithmic complexity depends on $n$) | communication ∝ bisection-limited all-to-all |
| Time growth under weak scaling | $\sim P^{1/3}\cdot\log P$ | $\sim P^{1/3}$ (torus) |
| "Fixed per-processor work" meaning | per iteration only | per rank only; network not constant |
| Fix | multigrid / preconditioning | 2-D (pencil) decomposition, topology-aware collectives, bigger grain |
