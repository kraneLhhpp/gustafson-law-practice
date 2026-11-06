# Task 02 — Derivation of Gustafson's Scaled Speedup

**Setting.** A program runs on $P$ identical processors. Measure on the *parallel* machine:

* $s$ — wall-clock time of the serial section (one processor works, the others wait),
* $p$ — wall-clock time of the parallel section (all $P$ processors work).

**Step 1 — normalisation.** Choose the time unit so that the parallel run takes exactly one unit:

$$T_P = s + p = 1 \qquad (1)$$

This is legitimate because the law is "fixed-time": we only care about *ratios* of times.
Consequently $s=\alpha$ is the serial fraction **of the parallel run**, and $p=1-\alpha$.

**Step 2 — work done by the parallel section.** For $p$ time units, $P$ processors each execute
useful work. Measured in "single-processor time units", that is

$$W_{par} = P\cdot p \qquad (2)$$

(assumption: parallel section is perfectly divisible, no overhead, processors identical).

**Step 3 — work done by the serial section.** One processor works for $s$ units:

$$W_{ser} = s \qquad (3)$$

**Step 4 — time of the equivalent serial run.** The same *scaled* problem, run on one processor, must do
all the work one after the other:

$$T_1 = W_{ser}+W_{par} = s + pP \qquad (4)$$

**Step 5 — speedup.** By definition, $S(P)=T_1/T_P$. With (1) and (4):

$$\boxed{S(P)=\frac{s+pP}{s+p}=s+pP} \qquad (5)$$

**Step 6 — express through $\alpha$.** Substitute $p=1-s$ and $s=\alpha$:

$$S(P)=\alpha+(1-\alpha)P=\alpha+P-\alpha P=\boxed{P-\alpha(P-1)} \qquad (6)$$

**Sanity checks.**

| Case | Result | Meaning |
|---|---|---|
| $P=1$ | $S=1$ | no speedup on one core |
| $\alpha=0$ | $S=P$ | embarrassingly parallel → linear |
| $\alpha=1$ | $S=1$ | purely serial → nothing gained |
| $dS/dP$ | $1-\alpha$ | *constant* slope: every extra core adds $(1-\alpha)$ useful cores |

**Efficiency:** $E(P)=S/P=1-\alpha\frac{P-1}{P}=(1-\alpha)+\frac{\alpha}{P}$.

**Assumptions used (and where):** (1) fixed wall time; (2),(4) perfectly divisible parallel work and
that the single-core run of the scaled problem would cost exactly $s+pP$ (no cache/memory effects);
(3) the serial part $s$ does not grow with the scaled problem size.
