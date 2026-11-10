"""Lab GM4-project-2: Rung 2 Completion Problem Twin — Macro Trade Sizing and Scenario Stress.

SIMULATED. Completed reference solution for the completion problem: implements
duration-neutral hedge ratio, net carry formula, fractional Kelly sizing, and payoff asymmetry.
"""

from __future__ import annotations

import numpy as np


def compute_hedge_ratio(dv01_1: float, dv01_2: float) -> float:
    """Completed: duration-neutral hedge ratio."""
    return dv01_1 / dv01_2


def compute_net_carry(yield_val: float, dur: float, roll_bps: float, repo: float, horizon: float) -> float:
    """Completed: net carry including roll-down and financing drag."""
    gross = yield_val * horizon
    roll = (roll_bps * 1e-4) * dur * horizon
    repo_drag = repo * horizon
    return gross + roll - repo_drag


def compute_kelly_weight(mu: float, var: float, fraction: float, cap: float) -> float:
    """Completed: fractional Kelly sizing with leverage cap."""
    raw = fraction * (mu / var)
    return max(-cap, min(cap, raw))


def compute_asymmetry(pnl: np.ndarray) -> float:
    """Completed: ratio of expected upside to expected downside."""
    u = np.maximum(0.0, pnl)
    d = np.maximum(0.0, -pnl)
    mu_u = float(np.mean(u))
    mu_d = float(np.mean(d))
    return mu_u / mu_d if mu_d > 1e-12 else float("inf")


def main() -> None:
    # Test fixture
    dv01_2y = 40.0
    dv01_10y = 80.0
    ratio = compute_hedge_ratio(dv01_2y, dv01_10y)

    net_carry_2y = compute_net_carry(0.045, 1.95, 6.0, 0.038, 0.5)
    net_carry_bps = net_carry_2y * 10_000.0

    k_weight = compute_kelly_weight(0.04, 0.0064, 0.25, 4.0)

    pnl_test = np.array([-0.05, -0.02, 0.03, 0.08, 0.12])
    asym_ratio = compute_asymmetry(pnl_test)

    print("=== Rung 2 Completed Solution Verification ===")
    print(f"Hedge Ratio: {ratio:.4f}")
    print(f"2Y Net Carry (bps): {net_carry_bps:.2f}")
    print(f"Quarter Kelly Leverage: {k_weight:.2f}x")
    print(f"Payoff Asymmetry Ratio: {asym_ratio:.3f}")


main()
