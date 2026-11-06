# Task 10 — Memory Growth vs. Scaled Speedup (3-D grid)

## Formulation

Weak scaling: $W(P)=P\cdot W(1)$. With $O(N^3)$ work per time step and a fixed number of steps, $W\propto N^3$, so
$N(P)^3=P\,N(1)^3$, i.e. $N(P)=N(1)\,P^{1/3}$.

Memory: $M(P)=cP$ with $c$ the per-node memory. Memory cap per node $c_{max}=32\ \text{GiB}=2^{35}$ B.
Let $b$ = bytes per grid point (8 B per double × number of arrays held). Total capacity constraint:

$$b\,N^3\le P\cdot c_{max}\;\Longrightarrow\;\boxed{N_{max}(P)=\left(\frac{P\cdot c_{max}}{b}\right)^{1/3}}$$

Per-node local block edge: $n_{loc}=(c_{max}/b)^{1/3}$, so $N_{max}=n_{loc}P^{1/3}$.

## Numbers

| $b$ (bytes/pt) | meaning | points/node | $n_{loc}$ | $N_{max}$ (P=64) | $N_{max}$ (P=512) |
|---:|---|---:|---:|---:|---:|
| 8 | 1 array, double | $2^{32}=4.29\times10^9$ | 1 625 | **6 502** | **13 004** |
| 16 | 2 arrays (e.g. $u^n,u^{n+1}$) | $2^{31}$ | 1 290 | 5 161 | 10 321 |
| 24 | 3 arrays | $1.43\times10^9$ | 1 127 | 4 508 | 9 016 |

Worked example, $b=8$, $P=64$: $N^3=64\cdot2^{35}/8=2^{38}=2.749\times10^{11}$ → $N=2^{38/3}\approx6502$.
$P=512$: $N^3=2^{41}$ → $N=2^{41/3}\approx13004$.

## Observations

* Going from 64 to 512 nodes (×8) only doubles $N$ ($8^{1/3}=2$). *Linear* dimension grows as $P^{1/3}$ — the mesh
  *resolution* improves slowly even though throughput grows linearly.
* In practice reduce capacity: ghost layers, MPI buffers, OS and I/O buffers → use ≈ 80–90 % of memory
  ($\times0.9^{1/3}\approx0.965$ on $N$).
* If "32 GB" means $32\times10^9$ B instead of GiB, all $N$ shrink by $\approx2.4\%$.
* For a compute-bound code whose time per step is constant under weak scaling (Gustafson) *and* whose memory also grows as $P$,
  the two constraints coincide ($W\propto M\propto P$) — this is the special case where Gustafson and Sun–Ni (Task 11) agree.
