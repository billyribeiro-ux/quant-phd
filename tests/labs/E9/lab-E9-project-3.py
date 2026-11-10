"""Project Lab 3 (Rung 3 check): Sovereign DSA and Fan Chart Panel Engine.

SIMULATED sovereign panel (N=100 paths, H=10 years). Standard library only.
Computes deterministic baseline, fan chart percentile distributions,
debt ceiling breach frequency, and terminal debt sustainability metrics.
"""

from __future__ import annotations

import random

SEED = 2026


def debt_dynamics_step(b_prev: float, r: float, g: float, s: float) -> float:
    """Compute one-period exact discrete-time debt-to-GDP ratio."""
    if g <= -1.0 or r <= -1.0:
        msg = f"Invalid rates: r={r}, g={g}"
        raise ValueError(msg)
    if b_prev < 0.0:
        msg = f"Invalid debt: {b_prev}"
        raise ValueError(msg)
    return ((1.0 + r) / (1.0 + g)) * b_prev - s


def primary_gap(b_target: float, r: float, g: float, s_actual: float) -> float:
    """Compute primary gap s* - s required to stabilize debt at b_target."""
    s_star = ((r - g) / (1.0 + g)) * b_target
    return s_star - s_actual


def simulate_panel(
    n_paths: int,
    horizon: int,
    b0: float,
    r_base: float,
    g_base: float,
    s_base: float,
    vol: float,
    seed: int,
) -> tuple[list[float], list[list[float]]]:
    """Generate deterministic baseline and Monte Carlo paths."""
    baseline = [b0]
    b_base = b0
    for _ in range(horizon):
        b_base = debt_dynamics_step(b_base, r_base, g_base, s_base)
        baseline.append(b_base)

    rng = random.Random(seed)
    paths: list[list[float]] = []
    for _ in range(n_paths):
        path = [b0]
        b_curr = b0
        for _ in range(horizon):
            r_t = r_base + rng.gauss(0.0, vol)
            g_t = g_base + rng.gauss(0.0, vol)
            s_t = s_base + rng.gauss(0.0, vol * 0.5)
            b_curr = debt_dynamics_step(b_curr, r_t, g_t, s_t)
            path.append(b_curr)
        paths.append(path)

    return baseline, paths


def main() -> None:
    b0 = 0.88  # 88% of GDP
    r_base = 0.035  # 3.5%
    g_base = 0.020  # 2.0%
    s_base = -0.010  # 1.0% deficit
    vol = 0.015  # 1.5% macroeconomic volatility
    ceiling = 1.05  # 105% debt ceiling
    horizon = 10
    n_paths = 100

    baseline, paths = simulate_panel(n_paths, horizon, b0, r_base, g_base, s_base, vol, SEED)

    # Fan chart percentiles at terminal year (t = 10)
    terminal_vals = sorted(p[-1] for p in paths)
    p10 = terminal_vals[int(0.10 * (n_paths - 1))]
    p50 = terminal_vals[int(0.50 * (n_paths - 1))]
    p90 = terminal_vals[int(0.90 * (n_paths - 1))]

    # Breach probability anytime across horizon
    breaches = sum(1 for p in paths if any(v > ceiling for v in p))
    p_breach = breaches / n_paths

    # Primary gap in baseline at t = 0
    init_gap = primary_gap(b0, r_base, g_base, s_base)

    print("=== Rung 3 Check: Sovereign DSA Engine Summary ===")
    print(f"Total Monte Carlo Trajectories:  {n_paths}")
    print(f"Horizon:                         {horizon} years")
    print(f"Initial Debt Ratio b0:           {b0:.4f}")
    print(f"Baseline Terminal Debt (t=10):   {baseline[-1]:.4f}")
    print(f"Baseline Initial Primary Gap:    {init_gap:.4f}")
    print("\nTerminal Debt Distribution (t=10):")
    print(f"  10th Percentile (P10):         {p10:.4f}")
    print(f"  50th Percentile (Median):      {p50:.4f}")
    print(f"  90th Percentile (P90):         {p90:.4f}")
    print(f"\nDebt Ceiling Threshold:          {ceiling:.4f}")
    print(f"Anytime Breach Probability:      {p_breach * 100.0:.2f}%")

    assert len(baseline) == 11, "Baseline must contain 11 points (t=0 to 10)"
    assert len(paths) == 100, "Must contain exactly 100 simulation paths"
    assert p10 < p50 < p90, "Percentiles must be strictly ordered"
    assert baseline[-1] > b0, "Baseline debt must increase when r > g and running deficit"


main()
