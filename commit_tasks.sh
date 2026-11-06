#!/bin/sh
# Atomic commits, one per task. Run from anywhere inside your git repo:  sh gustafson-law-practice/commit_tasks.sh
cd "$(dirname "$0")" || exit 1
c() { msg="$1"; shift; for f in "$@"; do [ -e "$f" ] || { echo "skip (missing): $f"; return; }; done
      git add -- "$@" && git commit -m "$msg" -q && echo "committed: $msg"; }
c "feat: complete task 01 scaling models"          theory/task01_scaling_models.md
c "feat: complete task 02 derivation"              theory/task02_derivation.md
c "feat: complete task 03 serial fraction invariance" theory/task03_serial_invariance.md
c "feat: complete task 04 asymptotic limits"       theory/task04_asymptotic_limits.md
c "feat: complete task 05 nCUBE case study"        theory/task05_historical_ncube.md
c "feat: complete task 06 parametric table"        calculations/task06_parametric_table.md
c "feat: complete task 07 tolerable serial fraction" calculations/task07_tolerable_serial.md
c "feat: complete task 08 amdahl vs gustafson"     calculations/task08_cross_divergence.md
c "feat: complete task 09 multicomponent workload" calculations/task09_multicomponent.md
c "feat: complete task 10 memory growth"           calculations/task10_memory_growth.md
c "feat: add numeric verification script and log"  calculations/verify_calculations.py calculations/numeric_log.txt
c "feat: complete task 11 Sun-Ni comparison"       theory/task11_sun_ni_comparison.md
c "feat: complete task 12 communication penalty"   theory/task12_communication_penalty.md
c "feat: complete task 13 failure cases"           theory/task13_failure_cases.md
c "feat: complete task 14 isoefficiency"           theory/task14_isoefficiency.md
c "feat: complete task 15 energy scaling"          theory/task15_energy_scaling.md
c "feat: complete task 16 GEMM scaling"            calculations/task16_gemm_scaling.md
c "feat: complete task 17 stencil scaling"         calculations/task17_stencil_scaling.md
c "feat: complete task 18 n-body scaling"          analysis/task18_nbody_scaling.md
c "feat: complete task 19 Monte Carlo"             analysis/task19_monte_carlo.md
c "feat: complete task 20 graph processing"        analysis/task20_graph_processing.md
c "feat: complete task 21 simulator"               benchmarks/simulator.py plots/speedup_table.csv plots/scaling_overlay.png plots/scaling_overlay.pdf
c "feat: complete task 22 weak-scaling benchmark"  benchmarks/weak_scale_bench
c "feat: complete task 23 fit script and results"  benchmarks/fit_gustafson.py benchmarks/results.csv
c "feat: complete task 24 plots and hardware audit" plots/make_plots.py benchmarks/collect_hw_info.sh analysis/task24_hardware_audit.md
c "docs: complete task 25 master README"           README.md .gitignore
