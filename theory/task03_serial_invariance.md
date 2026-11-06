# Task 03 — The Serial-Fraction "Invariance" Paradox

## Memo: frame of reference for measuring the serial fraction

**Notation.** Let $s_t$ = absolute serial time (same on 1 or $P$ cores) and $p_t$ = parallel-section
time **on the $P$-core machine** for the scaled problem.

* Gustafson's fraction — measured on the **parallel** machine:
  $$\alpha=\frac{s_t}{s_t+p_t}$$
* Amdahl's fraction — measured on the **uniprocessor** for the *same (scaled)* problem.
  The uniprocessor needs $P\,p_t$ for the parallel part:
  $$s_1=\frac{s_t}{s_t+P\,p_t}$$

## The apparent paradox

Amdahl says: with $s=0.4\%$ you can never exceed $250\times$. Gustafson's team observed $\approx1020\times$ on
1024 processors with "$s=0.4$–$0.8\%$". Both cannot be true if "$s$" means the same thing.

## Resolution — change of variables

Express $s_1$ through $\alpha$ (divide numerator and denominator by $s_t+p_t$):

$$s_1=\frac{\alpha}{\alpha+(1-\alpha)P}\qquad\Longleftrightarrow\qquad \alpha=\frac{P\,s_1}{1+(P-1)s_1}.$$

Insert $s_1$ into Amdahl's formula:

$$S_A=\frac{1}{s_1+\frac{1-s_1}{P}}
=\frac{1}{\frac{s_t}{s_t+Pp_t}+\frac{Pp_t}{P(s_t+Pp_t)}}
=\frac{s_t+Pp_t}{s_t+p_t}=s_t+Pp_t=P-\alpha(P-1).$$

So **Gustafson's Law is Amdahl's Law** evaluated with a *different, $P$-dependent* serial fraction
(this equivalence has been pointed out in the literature, e.g. Y. Shi, "Reevaluating Amdahl's Law and Gustafson's Law").

## Why the serial part no longer throttles scaling

* On the uniprocessor, the serial fraction of the *scaled* problem is $s_1\approx\dfrac{\alpha}{(1-\alpha)P}$ for large $P$ —
  it **shrinks like $1/P$**, because the problem got $P$ times bigger while $s_t$ did not.
* Amdahl's ceiling $1/s_1\approx(1-\alpha)P/\alpha$ therefore **grows linearly** with $P$ and never binds.
* Numerical example ($\alpha=0.08$, $P=128$): $s_1=0.08/(0.08+0.92\cdot128)=6.79\times10^{-4}$;
  Amdahl bound $1/s_1\approx1473$; actual speedup $117.84=128-0.08\cdot127$ ✔ (identical to Gustafson).

## Critical comment — the frame of reference is the whole story

| | Amdahl | Gustafson |
|---|---|---|
| Frame | Sequential machine | Parallel machine |
| $s$ depends on $P$? | No (problem fixed) | Yes, in disguise: $s_1(P)\propto1/P$ |
| Implied problem | Same for all $P$ | Grows with $P$ |
| Danger | Plugging a *small-problem* $s_1$ into a *big-machine* forecast → pessimism | Plugging a *parallel-run* $\alpha$ into a *strong-scaling* forecast → optimism |

The "invariance" is a modelling statement, not a theorem: it is true only if $s_t$ is independent of problem
size. If serial work grows with $n$ (e.g. serial I/O of the whole mesh), $\alpha$ is not constant and the
paradox reappears (see Tasks 12 and 13).
