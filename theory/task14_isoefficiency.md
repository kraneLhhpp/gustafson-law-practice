# Task 14 — Isoefficiency of a Gustafson-Compliant Program

## 1. Definitions (Grama, Gupta, Kumar)

* $W$ — problem size = time of the best serial algorithm, $W=T_1$.
* Overhead function $T_o(W,P)=P\,T_P-W$ (total time all processors spend not doing useful work).
* Efficiency $E=\dfrac{W}{P\,T_P}=\dfrac{1}{1+T_o/W}$.
* **Isoefficiency:** keep $E$ constant ⇒ $W=K\,T_o(W,P)$, $K=\dfrac{E}{1-E}$. The solution $W=f(P)$ is the *isoefficiency function*.

## 2. A Gustafson-compliant program

Model: serial section of constant absolute duration $s$ (independent of $W$); the remaining work $W-s$ perfectly parallel:

$$T_P=s+\frac{W-s}{P}.$$

**Overhead:**

$$T_o=P\,T_P-W=Ps+W-s-W=\boxed{s\,(P-1)}\quad\text{(independent of }W\text{).}$$

**Isoefficiency equation:** $W=K\,s\,(P-1)$ ⇒

$$\boxed{W(P)=\Theta(P)}$$

i.e. the isoefficiency function is **linear** — the best attainable.

## 3. Connection to Gustafson's formula

Take $T_P=s+p=1$ and $W=s+pP$ (Task 02). Then $T_o=s(P-1)$ and

$$E=\frac{W}{W+T_o}=\frac{s+pP}{s+pP+sP-s}=\frac{s+pP}{P(s+p)}=1-\alpha+\frac{\alpha}{P}\quad\text{(Task 04)}.$$

As $P\to\infty$, $W/T_o\to p/s=(1-\alpha)/\alpha$ constant ⇒ efficiency constant $=1-\alpha$. So *growing $W$ linearly with $P$* (Gustafson's fixed-time scaling)
**is** isoefficiency scaling for this overhead.
At the fixed-time operating point $p/s=(1-\alpha)/\alpha$ the sustained efficiency is $1-\alpha$. A *higher* target $E$ needs the same $\Theta(P)$ growth rate but a
larger constant $K=E/(1-E)$ in $W=Ks(P-1)$ — i.e. a larger grain per processor (and therefore a longer run time than the fixed-time budget).

## 4. Critique

* **Lower bound.** Any parallel system needs $W=\Omega(P)$ (otherwise some processors have no work); Gustafson scaling meets it, so it is *perfectly scalable* in the isoefficiency sense.
* **Contrast with Amdahl-type overhead** ($T_o=\sigma W(P-1)$, serial *fraction* fixed): $W=K\sigma W(P-1)$ ⇒ $1=K\sigma(P-1)$, no solution for large $P$ at fixed $E$ — **no isoefficiency function exists**; efficiency decays $\sim1/(\sigma P)$ (Task 04).
* **When fixed-time ≠ isoefficiency.** If $T_o$ is superlinear in $P$, e.g. adding $n$ numbers with a tree reduction ($T_o\approx2P\log P$), then $W=\Theta(P\log P)$ is needed.
  Constant time ($W\propto P$) would be *under*-scaling: efficiency decays like $1/\log P$ (Task 12). Gustafson weak scaling is therefore only a special case of isoefficiency, valid when overhead is $O(P)$.

## 5. Result

For a Gustafson-compliant weak-scaling program, $T_o=s(P-1)=\Theta(P)$ and the isoefficiency function is $\boxed{W=\Theta(P)}$, with asymptotic efficiency $1-\alpha$.
