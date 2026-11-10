"""CS6 Lab L01-1: Amdahl's Law, Gustafson's Law, and Karp-Flatt Metric Evaluation.

Standard library only. Evaluates theoretical vs communication-constrained parallel speedup,
efficiency degradation, and empirical serial fraction extraction.
"""

from __future__ import annotations

import math


def amdahl_speedup(serial_fraction: float, p_cores: int) -> float:
    """Compute theoretical strong scaling speedup via Amdahl's Law."""
    if p_cores < 1:
        raise ValueError("Core count must be at least 1.")
    return 1.0 / (serial_fraction + (1.0 - serial_fraction) / float(p_cores))


def gustafson_speedup(serial_fraction: float, p_cores: int) -> float:
    """Compute theoretical weak scaling speedup via Gustafson-Barsis Law."""
    if p_cores < 1:
        raise ValueError("Core count must be at least 1.")
    return serial_fraction + float(p_cores) * (1.0 - serial_fraction)


def karp_flatt_metric(speedup: float, p_cores: int) -> float:
    """Extract experimental serial fraction from observed speedup."""
    if p_cores <= 1:
        return 0.0
    return (1.0 / speedup - 1.0 / float(p_cores)) / (1.0 - 1.0 / float(p_cores))


def simulate_scaling_run() -> None:
    s = 0.05  # 5% serial fraction
    cores = [1, 2, 4, 8, 16, 32, 64]
    comm_coeff = 0.002  # O(log P) communication overhead

    print("=== CS6 Lab 1: Parallel Scaling & Karp-Flatt Metric Analysis ===")
    print(f"Serial fraction s = {s:.2f}, Asymptotic Amdahl limit S(inf) = {1.0 / s:.2f}x\n")
    header = (
        f"{'Cores':>6} | {'Amdahl':>8} | {'Gustafson':>10} | "
        f"{'Realistic':>10} | {'Efficiency':>10} | {'Karp-Flatt':>10}"
    )
    print(header)
    print("-" * 68)

    for p in cores:
        s_amdahl = amdahl_speedup(s, p)
        s_gustafson = gustafson_speedup(s, p)

        # Realistic runtime: T(p) = s + (1-s)/p + comm_coeff * log2(p)
        comm_overhead = comm_coeff * math.log2(p) if p > 1 else 0.0
        t_p = s + (1.0 - s) / float(p) + comm_overhead
        s_realistic = 1.0 / t_p
        efficiency = s_realistic / float(p)
        e_kf = karp_flatt_metric(s_realistic, p)

        eff_str = f"{efficiency * 100:9.1f}%"
        row = f"{p:6d} | {s_amdahl:8.3f} | {s_gustafson:10.3f} | {s_realistic:10.3f} | {eff_str} | {e_kf:10.4f}"
        print(row)


simulate_scaling_run()
