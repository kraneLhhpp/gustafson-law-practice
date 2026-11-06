# Task 12 — Gustafson with a Communication-Overhead Term

## 1. Model

Measure times on the $P$-core run in units where useful work is $s+p=1$ ($s=\alpha$). Add a **communication/synchronisation
penalty** $c(P)$ (same units; $c(1)=0$). The parallel run now takes $T_P=1+c(P)$. The equivalent one-core run has no
communication: $T_1=s+pP=P-\alpha(P-1)$. Therefore

$$\boxed{S_c(P)=\frac{P-\alpha(P-1)}{1+c(P)}},\qquad
E_c(P)=\frac{E_G(P)}{1+c(P)}=\frac{(1-\alpha)+\alpha/P}{1+c(P)}.$$

Equivalent *effective serial fraction* (what you would fit with Gustafson's formula, Task 23): define $\alpha_{eff}$ by
$S_c=P-\alpha_{eff}(P-1)$, i.e.

$$\alpha_{eff}(P)=\frac{P-S_c(P)}{P-1}.$$

For $c=0$ it equals $\alpha$; for $P\gg1$, $\alpha_{eff}\to1-\dfrac{1-\alpha}{1+c(P)}\approx\alpha+c(P)$ when both are small.
So **communication shows up in a regression as an $\alpha$ that grows with $P$** (the effective $\alpha$ for the numbers in Section 4 rises from 0.080 at $P=16$ to 0.158 for $\log P$ and 0.579 for $\sqrt P$ at $P=16384$).

## 2. Parametrisation of $c(P)$

$c(P)=\gamma_{lat}\log_2P+\gamma_{bw}\sqrt{P}+\gamma_0$, where

* $\log_2P$ — tree reduction / broadcast / barrier latency,
* $\sqrt P$ — 2-D mesh bisection effects, all-to-all on limited bisection (or 2-D decomposition collectives),
* $\gamma$ — ratio (comm time per level)/(useful time per processor); it is **inversely proportional to the per-processor grain size** $g$: $\gamma=\kappa/g$.

## 3. Asymptotics

| $c(P)$ | $S_c(P)$ for large $P$ | $E_c\to$ |
|---|---|---|
| $\gamma\log_2P$ | $\Theta\!\left(\dfrac{(1-\alpha)P}{\gamma\log_2P}\right)$ | 0 (slowly, $1/\log P$) |
| $\gamma\sqrt P$ | $\Theta\!\left(\dfrac{(1-\alpha)\sqrt P}{\gamma}\right)$ | 0 ($1/\sqrt P$) |
| constant $\gamma_0$ | $\dfrac{(1-\alpha)P}{1+\gamma_0}$ | $\dfrac{1-\alpha}{1+\gamma_0}$ |

So **any growing** $c(P)$ destroys the "efficiency plateau" of Gustafson's law (Task 04): $S$ is no longer $\Theta(P)$.

## 4. Numerical illustration ($\alpha=0.04$, $\gamma=0.01$)

| $P$ | $S_G$ | $S_c$, $c=\gamma\log_2P$ | $E$ | $S_c$, $c=\gamma\sqrt P$ | $E$ |
|---:|---:|---:|---:|---:|---:|
| 16 | 15.4 | 14.8 | 0.926 | 14.8 | 0.926 |
| 256 | 245.8 | 227.6 | 0.889 | 211.9 | 0.828 |
| 1 024 | 983.1 | 893.7 | 0.873 | 744.8 | 0.727 |
| 4 096 | 3 932.2 | 3 510.9 | 0.857 | 2 397.7 | 0.585 |
| 16 384 | 15 728.7 | 13 797.1 | 0.842 | 6 898.5 | 0.421 |

## 5. Restoring weak scaling

Since $\gamma=\kappa(P)/g$, keep $c$ bounded by **growing the grain** $g\propto\kappa(P)$ (e.g. $g\propto\log P$ or $\sqrt P$).
Work per processor then increases, so run time under "fixed work per processor" grows — a trade between constant time (Gustafson)
and constant efficiency (isoefficiency, Task 14). Alternatively, overlap communication with computation so that part of $c(P)$ is hidden.
