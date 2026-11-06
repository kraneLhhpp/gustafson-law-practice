# Task 01 — Strong Scaling vs. Weak Scaling: Amdahl (1967) vs. Gustafson (1988)

## 1. The two questions being asked

| | Amdahl (1967) | Gustafson–Barsis (1988) |
|---|---|---|
| Question | "How much **faster** can I solve *this* problem?" | "How much **bigger** a problem can I solve in *this* time?" |
| What is held constant | Total workload $W$ (problem size $n$) | Wall-clock time $T_P$ |
| What varies with $P$ | Time $T(P)$ shrinks | Workload $W(P)$ grows |
| Scaling regime | **Strong scaling** | **Weak scaling** |
| Serial part | Fixed *fraction* $s$ of the 1-core run | Fixed *absolute time* $s$ on the $P$-core run |
| Speedup | $S_A(P)=\dfrac{1}{s+(1-s)/P}$ | $S_G(P)=P-\alpha(P-1)=s+pP$ |
| Limit as $P\to\infty$ | $1/s$ (bounded) | $\sim(1-\alpha)P$ (unbounded, linear) |

## 2. Behaviour of the problem dimension as $P\to\infty$

**Amdahl (fixed-size).** $n$ is constant. The work per processor is $W/P\to 0$.
Execution time $T(P)=T(1)\,[\,s+(1-s)/P\,]\to s\,T(1)$: the parallel part vanishes and
the serial part is what remains. Processors become *starved*: each has less and less to do,
while the serial section is unchanged → speedup saturates at $1/s$.

**Gustafson (fixed-time).** $n=n(P)$ is chosen so that the parallel phase keeps taking the same
time on $P$ processors, i.e. work per processor is constant and $W(P)=s+pP\to\infty$ (linearly in $P$
if the parallel work is perfectly divisible). The serial time $s$ does **not** grow with $n$
(this is the key modelling assumption — it is typically I/O set-up, parameter parsing,
the root part of a reduction, etc.). Hence the serial fraction *of the parallel run*
stays at $\alpha=s/(s+p)$ and the processors remain busy.

## 3. Why "fixed-size" and "fixed-time"?

* Amdahl's Law takes the **input as given** ("fixed-size"): the experimenter compares the *same*
  program on the *same* input with 1 and with $P$ cores; time is the output.
* Gustafson's Law takes the **time budget as given** ("fixed-time", e.g. "the weather forecast must be
  ready in 1 h"); the problem resolution (grid size, number of particles, ...) is the output.
  Normalising $s+p=1$ encodes exactly this: the parallel run always takes one unit of time.

(Sun & Ni add a third regime — **fixed-memory** — see Task 11.)

## 4. Philosophical / physical divergence

1. **Who chooses the problem?** Amdahl: the problem is a given. Gustafson: the available machine
   shapes the problem ("one does not take a fixed-size problem and run it on varying numbers of processors
   except when doing academic research" — Gustafson's argument in CACM 1988).
2. **Where is the serial fraction measured?** Amdahl: on one processor. Gustafson: on the $P$-processor
   run. These are *different numbers* for the same program (Task 03), which is why the two laws look
   contradictory but are algebraically equivalent.
3. **Physical reality.** Scientific codes (PDE solvers, MD, Monte Carlo) have resolution knobs. More
   hardware → finer mesh / more particles / more samples. Serial work (set-up, I/O of a fixed-size
   input) does not scale with these knobs, so $\alpha$ shrinks as the problem grows.
4. **Where each is the right tool.** Amdahl: latency-bound problems with fixed size (a query, a
   frame, a real-time control loop). Gustafson: throughput/resolution-bound science and big-data work.

## 5. Caveats shared by both

Both models assume perfectly divisible parallel work and **zero** parallel overhead
(communication, load imbalance, contention). Tasks 12–14 and 20 relax this.
