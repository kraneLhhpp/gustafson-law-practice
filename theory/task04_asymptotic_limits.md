# Task 04 — Asymptotic Behaviour of Parallel Efficiency

## 1. Gustafson

$$E_G(P)=\frac{S_G(P)}{P}=\frac{P-\alpha(P-1)}{P}=1-\alpha+\frac{\alpha}{P}.$$

**Limit proof.** $\alpha/P\to0$ as $P\to\infty$ (α is a constant, $0\le\alpha\le1$). Hence

$$\boxed{\lim_{P\to\infty}E_G(P)=1-\alpha}$$

Moreover $E_G$ is strictly decreasing for $\alpha>0$ ($dE_G/dP=-\alpha/P^2<0$) and bounded below by $1-\alpha$.
It *never* goes to zero. Convergence is $O(1/P)$: $E_G(P)-(1-\alpha)=\alpha/P$.

## 2. Amdahl

$$E_A(P)=\frac{S_A(P)}{P}=\frac{1}{P\left(s+\frac{1-s}{P}\right)}=\frac{1}{sP+(1-s)}.$$

**Limit proof.** For $s>0$, denominator $sP+1-s\to\infty$, so

$$\boxed{\lim_{P\to\infty}E_A(P)=0},\qquad E_A(P)\sim\frac{1}{sP}\quad\text{(so }P\cdot E_A\to1/s\text{)}.$$

For $s=0$: $E_A\equiv1$.

## 3. Numerical contrast (serial fraction = 0.04)

| $P$ | $E_G$ | $E_A$ |
|---:|---:|---:|
| 16 | 0.9625 | 0.6250 |
| 1 024 | 0.96004 | 0.02385 |
| 16 384 | 0.960002 | 0.00152 |
| $10^6$ | 0.96000004 | $2.5\times10^{-5}$ |

## 4. Interpretation

* Under Gustafson, a fixed fraction of the processors is "wasted" waiting during the serial phase,
  *but that fraction doesn't grow*: efficiency plateaus at $1-\alpha$.
* Under Amdahl, the parallel part shrinks to nothing, so almost *all* processors idle almost *all* the time → $E\to0$.
* Efficiency alone does not tell you which regime you are in — you must state what is held constant
  (problem size vs. time) when quoting it.
