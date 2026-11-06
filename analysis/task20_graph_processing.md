# Task 20 — Why Weak Scaling Is Hard for Graph Analytics (BFS, PageRank)

Gustafson's law needs: (1) work per processor can be held constant by enlarging the problem, (2) overheads per processor stay constant,
(3) serial time does not grow. Dense linear algebra and stencils satisfy these approximately; power-law graphs violate each.

## 1. Comparison

| Property | Dense GEMM / stencil | BFS / PageRank on power-law graphs |
|---|---|---|
| Memory access | regular, unit-stride, prefetchable, compute-bound | random pointer-chasing, latency/bandwidth-bound, cache-hostile (TEPS ≪ peak) |
| Work per processor | determined by sub-domain size | determined by *edges in frontier*: data-dependent, changes level by level |
| Partitioning | geometric, small separators: surface ∝ $n^2$ vs volume ∝ $n^3$ | small-world graphs have no small balanced separators: a large fraction of edges is cut whatever you do |
| Communication per rank | nearest neighbour, constant | near all-to-all; volume ∝ edges per rank, not shrinking relative to compute |
| Load balance | uniform | hubs (degree $10^5$–$10^6$) create stragglers; a 1-D vertex partition gives some ranks orders of magnitude more edges |
| Synchronisation | one step / halo exchange | level-synchronous BFS: barrier + frontier exchange *per level* |
| Parallelism profile | constant | frontier tiny at first and last levels, huge in the middle ⇒ serial-like phases |

## 2. Mechanisms that inflate $\alpha_{eff}(P)$

1. **Frontier imbalance and tiny levels.** Diameter $O(\log n)$ ⇒ few levels; the first/last ones have almost no parallel work (a "serial fraction" that
   *does not shrink* with $n$), the middle ones are bursty. Per-level cost includes a global barrier/allreduce $\Theta(\log P)$ and a frontier all-to-all.
2. **Skewed degree distribution.** Hub vertices make per-rank work $\propto$ sum of degrees, with heavy tails; $\max_i w_i\gg\bar w$ so time is set by the slowest rank
   (Task 19 straggler term, but much larger). Fixes: 2-D (edge) partitioning, delegates / vertex splitting for hubs.
3. **Edge cut ≈ $(P-1)/P$.** Random-like graphs ⇒ nearly every edge crosses ranks. Messages are small and unpredictable ⇒ latency- and injection-rate-bound,
   and bisection bandwidth becomes the limit as in 3-D FFT (Task 13).
4. **Data-dependent synchronisation.** Atomic updates to visited bitmaps/parent arrays, duplicate discovery of vertices in the same level, and direction-optimising switches
   (top-down ↔ bottom-up) create contention that is not a function of the problem size you chose.
5. **Weak-scaling definition itself is ambiguous.** Fixing *edges per rank* does not fix *work per rank* (BFS touches every edge once but PageRank iterates; the number of
   levels/iterations grows with scale: BFS levels $\sim\log n$, convergence iterations are roughly constant but not guaranteed). "Constant time" is then not a property you can choose, so the law's
   premise (i)–(ii) cannot be enforced.

## 3. PageRank vs. BFS

* PageRank = repeated sparse mat-vec on a power-law matrix: iteration count about constant w.r.t. size, no frontier, easy to balance edges — **closer** to Gustafson, but still
  gather/scatter irregular access and a global reduction per iteration (convergence check).
* BFS is worse: variable parallelism per level, tiny messages, and a work-efficiency / direction-optimisation trade-off.

## 4. Evidence from benchmarks and practice

Graph500 (BFS) is defined with a weak-scaling "scale" parameter (graph doubles when you add a factor of two of resources) and reports TEPS (traversed edges per second); parallel efficiency
on large systems is typically far below that of Linpack-type codes, and best-performing implementations rely on 2-D decomposition, bit-vector frontiers, direction-optimising BFS and communication compression — i.e. algorithms re-designed to *reduce α_eff*, not just run more ranks.

## 5. Conclusion

For graph analytics the observed scaled speedup is normally **sub-linear** and α is *not constant*: $S\approx\dfrac{P(1-\alpha)}{1+c(P)}$ with $c(P)$ growing (imbalance, all-to-all, barriers).
Use Gustafson only as an upper-bound reference; use measured TEPS-vs-P and isoefficiency analysis (Task 14) for planning.
