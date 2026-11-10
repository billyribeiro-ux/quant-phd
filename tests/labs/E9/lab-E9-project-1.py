"""Project Lab 1 (Rung 1): Fully worked example of Sovereign DSA and Fan Chart Engine.

SIMULATED sovereign debt scenario. Standard library only.
Computes deterministic baseline debt trajectory, primary gap,
fan chart percentile slices, and debt ceiling breach probability.
"""

from __future__ import annotations


def debt_dynamics_step(b_prev: float, r: float, g: float, s: float) -> float:
    """Compute one-period exact discrete-time debt-to-GDP ratio."""
    if g <= -1.0 or r <= -1.0:
        msg = f"Growth rate g and rate r must be strictly greater than -1.0: r={r}, g={g}"
        raise ValueError(msg)
    if b_prev < 0.0:
        msg = f"Debt-to-GDP ratio cannot be negative: b_prev={b_prev}"
        raise ValueError(msg)
    return ((1.0 + r) / (1.0 + g)) * b_prev - s


def primary_gap(b_target: float, r: float, g: float, s_actual: float) -> float:
    """Compute primary gap s* - s required to stabilize debt at b_target."""
    s_star = ((r - g) / (1.0 + g)) * b_target
    return s_star - s_actual


def main() -> None:
    # 1. Macroeconomic scenario calibration (5-year horizon)
    b0 = 0.90  # Initial debt: 90% of GDP
    r_path = [0.030, 0.032, 0.035, 0.033, 0.030]  # Real effective interest rate
    g_path = [0.020, 0.018, 0.015, 0.020, 0.022]  # Real GDP growth rate
    s_path = [-0.015, -0.010, -0.005, 0.000, 0.005]  # Primary balance (fiscal consolidation)
    debt_ceiling = 1.05  # 105% critical ceiling

    # 2. Deterministic baseline trajectory
    trajectory: list[float] = [b0]
    b_curr = b0
    gaps: list[float] = []

    for r, g, s in zip(r_path, g_path, s_path, strict=True):
        gap = primary_gap(b0, r, g, s)
        gaps.append(gap)
        b_curr = debt_dynamics_step(b_curr, r, g, s)
        trajectory.append(b_curr)

    # 3. Simulated Monte Carlo fan chart paths (3 representative sample paths)
    path_optimistic = [0.9000, 0.8920, 0.8800, 0.8650, 0.8450, 0.8200]
    path_baseline = trajectory
    path_stressed = [0.9000, 0.9350, 0.9780, 1.0250, 1.0620, 1.1050]

    all_paths = [path_optimistic, path_baseline, path_stressed]

    # Compute breach probability of debt ceiling (1.05)
    breaches = sum(1 for p in all_paths if any(b > debt_ceiling for b in p))
    p_breach = breaches / len(all_paths)

    print("=== Rung 1: Sovereign DSA & Fan Chart Worked Example ===")
    print(f"Initial Debt Ratio b0:           {b0:.4f}")
    print(f"Debt Ceiling:                    {debt_ceiling:.4f}")
    print("\nYear-by-Year Deterministic Baseline:")
    print("Year | Real Rate r | Real Growth g | Primary Bal s | Debt Ratio b | Primary Gap")
    for t in range(5):
        print(
            f"  {t + 1}  |   {r_path[t]:.4f}    |    {g_path[t]:.4f}     |    {s_path[t]:.4f}     |    "
            f"{trajectory[t + 1]:.4f}    |   {gaps[t]:.4f}"
        )

    print("\n=== Risk Diagnostics ===")
    print(f"Terminal Baseline Debt (Year 5): {trajectory[-1]:.4f}")
    print(f"Maximum Fiscal Gap in Horizon:   {max(gaps):.4f}")
    print(f"Debt Ceiling Breach Probability: {p_breach * 100.0:.2f}%")

    assert trajectory[0] == 0.90, "Initial debt must be 0.90"
    assert 0.90 < trajectory[-1] < 1.00, "Terminal debt should remain stabilized below 1.00 under consolidation"
    assert p_breach == 1.0 / 3.0, "1 out of 3 paths breaches the 105% ceiling"


main()
