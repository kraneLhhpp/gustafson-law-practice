# Task 19 — Monte Carlo: the "Ideal" Weak-Scaling Workload (and where α still hides)

Monte Carlo integration/path simulation: $P$ ranks each draw $k$ samples; results are combined. Communication is one reduction; per-rank
work is exactly constant under weak scaling. Yet $\alpha>0$ in practice. Sources:

| Source | Scaling | Remarks |
|---|---|---|
| **Start-up / input** (read input deck, cross-section tables, broadcast) | serial read + $O(\log P)$ broadcast | classic Gustafson $s$; constant if input is fixed-size |
| **PRNG stream creation** | naive loop on rank 0: $O(P)$; skip-ahead (LCG/leapfrog): $O(\log n)$ per rank, parallel; **counter-based** (Philox, Threefry): $O(1)$, no coordination | *Correctness issue too*: `seed=rank` with a weak generator gives correlated streams; use independent-stream methods (SplitMix, jump-ahead, SeedSequence/`spawn`). |
| **Reduction** of tallies | tree: $\lceil\log_2P\rceil\,(t_\ell+m\,t_b)$; flat gather to root: $P\,(t_\ell+m\,t_b)$ | $m$ = tally size (histogram bins!) |
| **Output serialisation** | $O(\text{output})$ on one rank | often the largest single contributor |
| **Load imbalance / stragglers** | $\propto\sigma\sqrt{2\ln P}$ (expected max of $P$ i.i.d. times) | variable path lengths (absorption, branching), OS noise |

## Quantifying the reduction

Model: $T_P=T_w(1+\varepsilon\sqrt{2\ln P})+t_{red}\lceil\log_2P\rceil+t_{out}$ (with $T_w$ = useful time per rank).
Weak-scaling speedup measured as $S=P\,T_1/T_P$; in Gustafson form $\alpha_{eff}=(T_P-T_w)/T_P$ (non-parallel share).

Example: $T_w=100$ s, $P=65\,536$, $t_{red}=50\ \mu$s per tree level (small message).

| Overhead | Time | $\alpha_{eff}$ | $S(P)=P-\alpha(P-1)$ | Efficiency |
|---|---:|---:|---:|---:|
| tree reduction ($16$ levels) | 0.8 ms | $8.0\times10^{-6}$ | 65 535.5 | 99.9992 % |
| **flat** reduction (gather, $P\cdot50\,\mu$s) | 3.28 s | 0.0317 | 63 457 | 96.8 % |
| serial output of 0.5 s | 0.5 s | 0.0050 | 65 210 | 99.5 % |
| stragglers, $\varepsilon=1\,\%$ ($\sqrt{2\ln P}=4.71$) | +4.7 % of $T_w$ | ≈0.045 | ≈62 590 | ≈95.5 % |

**Conclusions.**

1. A *tree* reduction costs only $O(\log P)$ — for realistic latencies it is invisible: $S_{tree}(P)=\dfrac{P-\alpha(P-1)}{1+\rho\log_2P}$ with $\rho=t_{red}/T_P\sim5\times10^{-7}$.
   Replacing it by a flat gather is 4 000× worse.
2. The real killers are (a) **serialised I/O**, (b) **load imbalance**, (c) **reductions of large tallies** (bandwidth term $m\,t_b\log P$, or $m\cdot P$ if gathered).
3. Mitigation: counter-based RNGs, hierarchical (node-level then global) reductions, `MPI_Reduce` with large-message algorithms (reduce-scatter+gather),
   parallel/collective I/O, dynamic batching of histories to rebalance.
4. Because α is tiny and independent of the sample count, Monte Carlo is the textbook case where $E\to1-\alpha\approx1$ — the reference curve against which
   other workloads (Tasks 16–20) are judged.
