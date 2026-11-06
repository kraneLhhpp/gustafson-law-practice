# weak_scale_bench — empirical weak-scaling harness (Tasks 22–23)

Workload: midpoint integration of $4/(1+x^2)$ over $[0,1]$ (→ π). **Each thread always processes `k` intervals**; global size is `P·k`.
Scaled speedup is reported as $S(P)=P\,T_1/T_P$ (Gustafson measure).

## Option A — Python (multiprocessing, needs numpy)

```bash
cd benchmarks
python3 -m pip install numpy matplotlib
python3 weak_scale_bench/weak_scale_bench.py --runs 5 --out results.csv            # 1,2,4,.. up to your hardware threads
python3 weak_scale_bench/weak_scale_bench.py --threads 1,2,4,8,12,16 --k 30000000   # explicit list (≥5 values for Task 23)
```

## Option B — C++ / OpenMP (recommended for cleaner numbers)

```bash
cd benchmarks/weak_scale_bench
g++ -O3 -march=native -fopenmp weak_scale_omp.cpp -o weak_scale_omp
OMP_PROC_BIND=close OMP_PLACES=cores ./weak_scale_omp --runs 5 --k 200000000 --out ../results.csv
```
(Pick `--k` so that the 1-thread run takes ≈ 1–2 s.)

## Validate the pipeline first

Both programs accept `--serial-frac f`, which injects a constant serial phase so that the *true* α equals `f`:

```bash
python3 weak_scale_bench/weak_scale_bench.py --serial-frac 0.05 --out /tmp/check.csv
python3 fit_gustafson.py --csv /tmp/check.csv --outdir /tmp/check     # alpha_observed should come out ≳ 0.05
```
(On a machine with turbo/SMT/NUMA effects the fit returns 0.05 *plus* those effects — that is exactly the discrepancy Task 24 asks you to explain.)

## Then fit and plot

```bash
cd benchmarks && python3 fit_gustafson.py          # -> summary.csv, fit_results.json (α_observed ± se)
cd ../plots && python3 make_plots.py               # -> scaling_comparison.pdf / .png
```

CSV columns: `threads,run,k_per_worker,serial_frac_injected,wall_s,pi_estimate`.
Timed region: serial phase + dispatch + parallel loop + reduction; pool creation and one warm-up run are excluded.
