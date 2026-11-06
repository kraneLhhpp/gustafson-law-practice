#!/usr/bin/env python3
"""Recomputes every number used in calculations/task06..task10, task16, task17 and prints a log.
   Run:  python3 verify_calculations.py | tee numeric_log.txt"""
import math

G = lambda P, a: P - a * (P - 1)           # Gustafson scaled speedup
A = lambda P, s: 1 / (s + (1 - s) / P)      # Amdahl fixed-size speedup

print("== Task 06: alpha = 0.04 ==")
for P in (16, 64, 256, 1024, 4096, 16384):
    S = G(P, 0.04)
    print(f"P={P:6d}  alpha(P-1)={0.04*(P-1):8.2f}  S={S:10.2f}  E={S/P:.6f}")

print("\n== Task 07: P=8192, S>=7500 ==")
a_max = (8192 - 7500) / (8192 - 1)
print(f"alpha_max = 692/8191 = {a_max:.7f}   S(alpha_max) = {G(8192, a_max):.4f}")
print(f"S(0.0844) = {G(8192, 0.0844):.2f}   S(0.0845) = {G(8192, 0.0845):.2f}")

print("\n== Task 08: s = alpha = 0.08 ==")
sa, sg = A(128, 0.08), G(128, 0.08)
print(f"P=128: Amdahl={sa:.4f}  Gustafson={sg:.2f}  ratio={sg/sa:.3f}  excess={100*(sg-sa)/sa:.1f}%  under-prediction={100*(sg-sa)/sg:.1f}%")
s1 = 0.08 / (0.08 + 0.92 * 128)
print(f"equivalent uniprocessor serial fraction s1 = {s1:.6e};  Amdahl(s1) = {A(128, s1):.4f}")
for P in (2, 8, 32, 128, 512, 2048, 8192, 65536):
    print(f"  P={P:6d}  S_A={A(P,0.08):8.3f}  S_G={G(P,0.08):10.3f}  ratio={G(P,0.08)/A(P,0.08):9.2f}")

print("\n== Task 09: alpha = 0.02 + 0.06 ==")
for P in (512, 2048):
    print(f"P={P}: S={G(P,0.08):.2f}  E={G(P,0.08)/P:.4f}   (only A serial: S={G(P,0.02):.2f})")

print("\n== Task 10: N_max = (P * 32GiB / b)^(1/3) ==")
for b in (8, 16, 24):
    print(f"b={b:2d} B/pt  n_loc={(32*2**30/b)**(1/3):7.1f}  " +
          "  ".join(f"P={P}: N={(P*32*2**30/b)**(1/3):9.1f}" for P in (64, 512)))

print("\n== Task 16: N(P) = 2048 * P^(1/3) ==")
for P in (1, 8, 16, 64, 128, 512, 1024, 4096, 32768):
    N = 2048 * P ** (1 / 3)
    print(f"P={P:6d}  N={N:9.1f}  mem/node={3*8*N*N/P/1e6:7.2f} MB  comm/comp growth P^(1/6)={P**(1/6):.3f}")

print("\n== Task 17: per-rank comm/comp ~ 6/n ==")
for P in (1, 8, 64, 512, 4096):
    print(f"P={P:5d}  weak n=256 -> {6/256:.4f}   strong N=1024 -> n={1024/P**(1/3):6.1f}  6/n={6/(1024/P**(1/3)):.4f}")
