# Task 07 — Maximum Tolerable Serial Fraction

Given $P=8192$, requirement $S(P)\ge7500$.

**Derivation.**

$$P-\alpha(P-1)\ge S_{req}\;\Longleftrightarrow\;\alpha(P-1)\le P-S_{req}\;\Longleftrightarrow\;\alpha\le\frac{P-S_{req}}{P-1}$$

(the inequality keeps its direction because $P-1>0$).

**Numbers.**

$$\alpha_{max}=\frac{8192-7500}{8192-1}=\frac{692}{8191}=0.0844830\ldots\approx\boxed{8.448\%}$$

**Check.** $S(\alpha_{max})=8192-\frac{692}{8191}\cdot8191=8192-692=7500$ ✔ (exact).
With a rounded-down value $\alpha=0.0844$: $S=8192-0.0844\cdot8191=7500.68\ge7500$ ✔.
With a rounded-up $\alpha=0.0845$: $S=7499.86<7500$ ✘ — so **round down**.

**Equivalent efficiency requirement:** $E\ge7500/8192=0.91553$; $E=1-\alpha+\alpha/P\Rightarrow\alpha\le(1-E)\frac{P}{P-1}$ gives the same bound.

**Comment.** Note how *tolerant* the weak-scaling target is: an 8.4 % serial fraction still gives 91.6 % efficiency on 8192 cores.
The same 8.4 % under Amdahl would cap speedup at ≈11.8×.
