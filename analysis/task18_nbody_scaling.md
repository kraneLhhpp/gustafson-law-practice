# Task 18 — N-Body Scaling: Direct $O(N^2)$ vs. Barnes–Hut $O(N\log N)$

## 1. Constant time per iteration ⇒ how must $N$ grow with $P$?

Ideal per-iteration time $T=W(N)/P$. Keep $T=T_1$ (the 1-processor time for base size $N_1$).

| | Work $W(N)$ | Condition | Required growth |
|---|---|---|---|
| Direct all-pairs | $cN^2$ | $N^2/P=N_1^2$ | $N=N_1\sqrt P$ |
| Barnes–Hut | $cN\log N$ | $N\log N=P\,N_1\log N_1$ | $N\approx\dfrac{P\,N_1\log N_1}{\log N}=\Theta\!\left(\dfrac{P}{\log P}\right)$ (sub-linear in $P$) |

Example ($N_1=10^5$): 

| $P$ | $N_{direct}$ | $N_{BH}$ | $N_{BH}/(P N_1)$ |
|---:|---:|---:|---:|
| 64 | 800 000 | 4.79 M | 0.75 |
| 1 024 | 3.2 M | 65.5 M | 0.64 |
| 16 384 | 12.8 M | 914 M | 0.56 |

(The BH problem grows almost linearly in $P$; direct only as $\sqrt P$, i.e. the same machine buys a much smaller particle increase.)

## 2. How the serial/overhead ratio shifts

**Direct method.** Compute per rank is constant by construction, but each rank needs *all* $N$ positions (all-gather / ring pass):
communication volume per rank $\Theta(N)=\Theta(\sqrt P)$ and replicated memory $\Theta(N)$.

$$\frac{t_{comm}}{t_{comp}}=\Theta(\sqrt P)\;\Rightarrow\;c(P)=\gamma\sqrt P\ \text{(Task 12)}$$

⇒ Efficiency decays like $1/\sqrt P$. With $\gamma=0.01$, $P=16384$: $c=1.28$, efficiency ≈ 44 % even for $\alpha=0$.
Weak scaling at constant time is only *nominal* — the all-to-all data dependence breaks the premise (Task 13).

**Barnes–Hut.** Per-rank compute again constant. Overheads: (i) tree build and domain decomposition (parallel sort / ORB): $O(\log P)$ global
steps; (ii) top levels of the tree are replicated: $O(\log P)$ nodes; (iii) "locally essential tree" exchange: $\Theta\bigl((N/P)^{2/3}\bigr)+\Theta(\log P)$ per rank —
surface-to-volume like (Task 17); (iv) load imbalance from clustered particles (dominant in practice).

$$c(P)=\Theta(\log P)\ \Rightarrow\ E\sim\frac{1-\alpha}{1+\gamma\log P}\ \text{— slow decay.}$$

## 3. Summary

| Quantity | Direct | Barnes–Hut |
|---|---|---|
| $N(P)$ at constant time | $\propto\sqrt P$ | $\propto P/\log P$ |
| Per-rank comm growth | $\sqrt P$ | $\log P$ (+ imbalance) |
| α-like overhead trend | grows quickly | grows slowly |
| Memory per rank | $O(\sqrt P)$ (replicated) | $O(N/P)$ |
| Gustafson usable? | no (needs ring-systolic tricks; still $\sqrt P$ bandwidth) | yes, approximately |

Take-away: *algorithmic* complexity decides whether "keep work per processor constant" is also "keep communication per processor constant". It is for stencils/BH; it is not for all-pairs.
