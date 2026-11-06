# Task 08 — Amdahl vs. Gustafson at $s=\alpha=0.08$, $P=128$

**Amdahl.**
$$S_A=\frac{1}{0.08+\frac{0.92}{128}}=\frac{1}{0.08+0.0071875}=\frac1{0.0871875}=11.4695$$

**Gustafson.**
$$S_G=128-0.08\cdot127=128-10.16=117.84$$

**Discrepancy.**

* Ratio $S_G/S_A=117.84/11.4695=10.27$.
* $S_G$ exceeds $S_A$ by $\dfrac{117.84-11.4695}{11.4695}=\mathbf{927\%}$.
* Equivalently, Amdahl *under*-predicts Gustafson by $\dfrac{117.84-11.47}{117.84}=\mathbf{90.3\%}$.

## Divergence with $P$ (same 0.08 in both formulas)

| $P$ | $S_A$ | $S_G$ | $S_G/S_A$ |
|---:|---:|---:|---:|
| 2 | 1.852 | 1.920 | 1.04 |
| 8 | 5.128 | 7.440 | 1.45 |
| 32 | 9.195 | 29.52 | 3.21 |
| 128 | 11.470 | 117.84 | 10.27 |
| 512 | 12.225 | 471.12 | 38.54 |
| 2 048 | 12.430 | 1 884.24 | 151.59 |
| 8 192 | 12.482 | 7 536.72 | 603.78 |
| 65 536 | 12.498 | 60 293.20 | 4 824.3 |

($S_A\to1/0.08=12.5$ while $S_G\sim0.92P$.) The ratio grows $\propto P$ asymptotically: $S_G/S_A\to0.92P\cdot0.08=0.0736P$.

## Why they diverge

They answer different questions about different problems:

* Amdahl's 0.08 is 8 % of the **single-core time of a fixed problem** → serial time stays 8 % of $T(1)$ forever.
* Gustafson's 0.08 is 8 % of the **$P$-core time of a $P$-times bigger problem** → its single-core equivalent is only
  $s_1=0.08/(0.08+0.92\cdot128)=6.79\times10^{-4}$ (0.068 %).
  Feeding $s_1$ to Amdahl reproduces 117.84 exactly (Task 03).

**Important:** the two numbers are *not* a "same program, two predictions" comparison. Using the same
numeric value 0.08 in both laws assumes two different physical situations. The 927 % gap is the price of getting the frame of
reference wrong.
