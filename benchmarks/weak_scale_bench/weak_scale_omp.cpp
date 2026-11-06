// Task 22 - Weak-scaling benchmark (OpenMP). Same workload and CSV format as weak_scale_bench.py.
//
//   g++ -O3 -march=native -fopenmp weak_scale_omp.cpp -o weak_scale_omp
//   OMP_PROC_BIND=close OMP_PLACES=cores ./weak_scale_omp --threads 1,2,4,8 --runs 5 --k 200000000 --out ../results.csv
//
// Per-thread work is constant: N = P*K midpoints of 4/(1+x^2) on [0,1].
// --serial-frac f injects a serial phase of K_s = f/(1-f)*K evaluations (constant in P) for validating the fit.
#include <omp.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <sstream>

static volatile double g_sink;

static double integrate_serial(long n) {            // n midpoints, sequential
    const double h = 1.0 / (double)n;
    double s = 0.0;
    for (long i = 0; i < n; ++i) { double x = ((double)i + 0.5) * h; s += 4.0 / (1.0 + x * x); }
    return s * h;
}

static double integrate_parallel(long n) {
    const double h = 1.0 / (double)n;
    double s = 0.0;
#pragma omp parallel for reduction(+ : s) schedule(static)
    for (long i = 0; i < n; ++i) { double x = ((double)i + 0.5) * h; s += 4.0 / (1.0 + x * x); }
    return s * h;
}

int main(int argc, char** argv) {
    long k = 200000000L; int runs = 5; double sf = 0.0; std::string out = "../results.csv";
    std::vector<int> threads;
    for (int i = 1; i < argc; ++i) {
        std::string a = argv[i];
        auto next = [&]() -> std::string { if (i + 1 >= argc) { fprintf(stderr, "missing value for %s\n", a.c_str()); exit(1); } return argv[++i]; };
        if (a == "--k") k = atol(next().c_str());
        else if (a == "--runs") runs = atoi(next().c_str());
        else if (a == "--serial-frac") sf = atof(next().c_str());
        else if (a == "--out") out = next();
        else if (a == "--threads") { std::stringstream ss(next()); std::string t; while (std::getline(ss, t, ',')) threads.push_back(atoi(t.c_str())); }
        else { fprintf(stderr, "unknown option %s\n", a.c_str()); return 1; }
    }
    const int maxT = omp_get_max_threads();
    if (threads.empty()) { for (int p = 1; p < maxT; p *= 2) threads.push_back(p); threads.push_back(maxT); }
    const long ks = sf > 0 ? (long)(sf / (1.0 - sf) * (double)k + 0.5) : 0;

    FILE* f = fopen(out.c_str(), "w");
    if (!f) { perror("open output"); return 1; }
    fprintf(f, "threads,run,k_per_worker,serial_frac_injected,wall_s,pi_estimate\n");
    fprintf(stderr, "max threads %d, k=%ld, runs=%d, k_serial=%ld\n", maxT, k, runs, ks);

    for (int P : threads) {
        omp_set_num_threads(P);
        for (int r = 0; r <= runs; ++r) {              // r = 0 is an unrecorded warm-up
            double t0 = omp_get_wtime();
            if (ks) g_sink = integrate_serial(ks);
            double pi = integrate_parallel((long)P * k);
            double t = omp_get_wtime() - t0;
            if (r == 0) continue;
            fprintf(f, "%d,%d,%ld,%g,%.6f,%.12f\n", P, r, k, sf, t, pi);
            fprintf(stderr, "P=%3d run=%d %9.4fs pi=%.12f\n", P, r, t, pi);
        }
    }
    fclose(f);
    fprintf(stderr, "wrote %s\n", out.c_str());
    return 0;
}
