# Task 15 — Energy under Gustafson Scaling

## 1. Model

* $P_{idle}$ — power a node draws whenever it is powered on (static).
* $P_{dyn}$ — *additional* power while it computes ($P_{active}=P_{idle}+P_{dyn}$).
* Wall-clock time $T$ (fixed). Serial phase $\alpha T$: 1 node computes, $P-1$ nodes are idle but powered. Parallel phase $(1-\alpha)T$: all $P$ compute.

**Energy on $P$ nodes (scaled problem of size $W=S(P)$ units, one unit = work of the 1-node job):**

$$E_P=\underbrace{P\,P_{idle}\,T}_{\text{static, all nodes, whole run}}+\underbrace{P_{dyn}\,T\,[\alpha+(1-\alpha)P]}_{=P_{dyn}\,T\,S(P)\ \text{(dynamic)}}$$

Dynamic energy is proportional to the **work done**; static energy is proportional to **node-time paid for**.

## 2. Comparison with one core

**(a) Same wall-clock time $T$, 1 core:** it can do only $W=1$ unit: $E_1=(P_{idle}+P_{dyn})T$.
Energy **per unit of work**:

$$\frac{E_1}{1}=(P_{idle}+P_{dyn})T,\qquad \frac{E_P}{S(P)}=T\Bigl[\frac{P_{idle}}{E_{eff}(P)}+P_{dyn}\Bigr]$$

where $E_{eff}=S/P=1-\alpha+\alpha/P$ is the parallel efficiency. The dynamic term is unchanged; the static term is inflated by $1/E_{eff}\to1/(1-\alpha)$.

**(b) Same *scaled* work, 1 core** (takes $S(P)\,T$): $E_1'=(P_{idle}+P_{dyn})\,S(P)\,T$. The difference is purely static:

$$E_P-E_1'=P_{idle}\,T\,(P-S)=\boxed{P_{idle}\,T\,\alpha\,(P-1)}$$

— the energy burnt by the $P-1$ idle nodes during the serial phase.

## 3. Numerical example

$P_{idle}=100$ W, $P_{dyn}=150$ W, $\alpha=0.04$, $P=1024$, $S=983.08$, $E_{eff}=0.96004$, $T=1$ h:

| | Energy (W·h) |
|---|---:|
| $E_P$ = $1024\cdot100+150\cdot983.08$ | 249 862 |
| $E_1'$ = $250\cdot983.08$ | 245 770 |
| Difference = $100\cdot0.04\cdot1023$ | 4 092 (+1.7 %) |

Per unit work: 254.2 W·h vs 250 W·h on one core (+1.7 %).

## 4. Interpretation

* With **perfect power proportionality** ($P_{idle}=0$) energy is identical (parallel run does the same work; faster, same joules).
* Real servers idle at 40–60 % of peak ⇒ the serial fraction costs energy proportional to $P\alpha$ idle node-seconds. Parallelism buys **time**, not joules.
* Mitigations: power-gate/ DVFS idle nodes during serial phases, overlap or pipeline serial I/O, reduce $\alpha$.
* Under Amdahl (strong scaling) the picture is worse: static energy grows as $P\,P_{idle}\,T(P)$ while $T(P)$ stops shrinking, so energy → ∞ linearly with $P$.
