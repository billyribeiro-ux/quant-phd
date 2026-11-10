"""Lab MS4-project-2: Rung 2 completion problem · Capacity calibration solver.

Completed twin for Rung 2. Computes the aggregate friction coefficient kappa,
derives optimal AUM under square-root impact, and filters assets through buffer hysteresis.
SIMULATED: 4-asset portfolio verification check.
"""

from __future__ import annotations

import math


def calculate_friction_kappa(
    w_initial: list[float],
    w_target: list[float],
    adv: list[float],
    sigma: list[float],
    prefactor_y: float = 0.5,
) -> float:
    """Compute aggregate portfolio market impact friction coefficient."""
    n = len(w_initial)
    friction = float(
        prefactor_y * sum(sigma[i] * (abs(w_target[i] - w_initial[i]) ** 1.5) / math.sqrt(adv[i]) for i in range(n))
    )
    return friction


def solve_capacity_limits(gross_alpha: float, kappa: float) -> tuple[float, float, float]:
    """Solve for break-even AUM, profit-maximizing AUM, and max dollar alpha."""
    breakeven_aum = (gross_alpha / kappa) ** 2
    optimal_aum = (4.0 / 9.0) * breakeven_aum
    max_dollar_alpha = (4.0 / 27.0) * (gross_alpha**3) / (kappa**2)
    return breakeven_aum, optimal_aum, max_dollar_alpha


def apply_buffer_retention(
    ranks: list[float],
    current_weights: list[float],
    target_k: int,
    buffer_ratio: float = 1.5,
) -> list[float]:
    """Select holdings with buffer-zone hysteresis."""
    n = len(ranks)
    k_hold = math.floor(target_k * buffer_ratio)
    is_held = [w > 1e-6 for w in current_weights]
    retained = [i for i in range(n) if is_held[i] and ranks[i] <= k_hold]
    retained.sort(key=lambda idx: ranks[idx])

    if len(retained) >= target_k:
        selected = retained[:target_k]
    else:
        needed = target_k - len(retained)
        unheld = [i for i in range(n) if i not in retained]
        unheld.sort(key=lambda idx: ranks[idx])
        selected = retained + unheld[:needed]

    weights = [0.0] * n
    for idx in selected:
        weights[idx] = 1.0 / target_k
    return weights


def run_completion_check() -> None:
    w_init = [0.25, 0.25, 0.25, 0.25]
    w_tgt = [0.40, 0.10, 0.30, 0.20]
    adv = [20000000.0, 15000000.0, 30000000.0, 25000000.0]
    sigma = [0.020, 0.025, 0.018, 0.022]
    alpha = 0.09
    prefactor = 0.50

    kappa = calculate_friction_kappa(w_init, w_tgt, adv, sigma, prefactor)
    a_star, a_opt, max_d = solve_capacity_limits(alpha, kappa)

    ranks = [1.0, 4.0, 2.0, 3.0]
    target_k = 2
    weights = apply_buffer_retention(ranks, w_init, target_k, buffer_ratio=1.5)

    print(f"Friction Kappa:     {kappa:.8e}")
    print(f"Break-even AUM A*:  {a_star:.2f}")
    print(f"Optimal AUM A_opt:  {a_opt:.2f}")
    print(f"Max Dollar Alpha:   {max_d:.2f}")
    print(f"Selected Weights:   {weights}")
    print(f"Valid Probability:  {math.isclose(sum(weights), 1.0, abs_tol=1e-5)}")


def main() -> None:
    run_completion_check()


main()
