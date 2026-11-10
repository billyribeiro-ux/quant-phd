"""AC3 lab L06: voluntary disclosure equilibrium and unraveling under information uncertainty.

SIMULATED: the voluntary disclosure game of Dye (1985) and Jung & Kwon (1988) with uniform
prior on firm value v ~ U[0, 1], information arrival probability p, and proprietary cost c.
Solves the equilibrium disclosure cutoff v* and silence pricing P_silent analytically and
verifies with fixed-point iteration. Standard library math and float only.
"""

from __future__ import annotations

import math

SEED = 20261110


def solve_dye_cutoff(p: float, c: float) -> tuple[float, float]:
    """Solve equilibrium disclosure cutoff v* and silence price P_silent for v ~ U[0, 1].

    Cutoff satisfies 0.5 * p * (v*)^2 + (1 - p - p * c) * v* - (0.5 + c) * (1 - p) = 0.
    Returns (v_star, p_silent).
    """
    coeff_a = 0.5 * p
    coeff_b = (1.0 - p) - p * c
    coeff_c = -(0.5 + c) * (1.0 - p)

    if coeff_a == 0.0:
        # p = 0: no information ever arrives
        v_star = 1.0
        p_silent = 0.5
        return v_star, p_silent

    discriminant = coeff_b * coeff_b - 4.0 * coeff_a * coeff_c
    if discriminant < 0:
        raise ValueError(f"Negative discriminant: {discriminant}")

    v_star = (-coeff_b + math.sqrt(discriminant)) / (2.0 * coeff_a)
    # Clip to valid domain [0, 1]
    v_star = max(0.0, min(1.0, v_star))
    p_silent = v_star - c
    return v_star, p_silent


def verify_fixed_point(v_star: float, p: float, c: float) -> float:
    """Evaluate difference between v* - c and conditional expectation E[v | silence]."""
    num = 0.5 * (1.0 - p) + 0.5 * p * (v_star**2)
    denom = (1.0 - p) + p * v_star
    e_silent = num / denom if denom > 0 else 0.5
    return abs((v_star - c) - e_silent)


def main() -> None:
    print(f"seed {SEED} dye_jung_kwon_disclosure_equilibrium")
    print(f"{'p (prob)':8s} | {'c (cost)':8s} | {'v* (cutoff)':11s} | {'P_silent':10s} | {'Fixed_pt_err':12s}")
    print("-" * 60)

    # 1. Varying information probability p with zero proprietary cost c = 0
    c_zero = 0.0
    probs = [0.10, 0.30, 0.50, 0.70, 0.90, 0.99]
    cutoffs_p: list[float] = []

    for p in probs:
        v_star, p_sil = solve_dye_cutoff(p, c_zero)
        err = verify_fixed_point(v_star, p, c_zero)
        cutoffs_p.append(v_star)
        print(f"{p:8.2f} | {c_zero:8.2f} | {v_star:11.4f} | {p_sil:10.4f} | {err:12.2e}")

    # Check unravelling property: as p -> 1, cutoff v* -> 0 (Milgrom-Grossman full unraveling)
    print("-" * 60)
    is_decreasing = all(cutoffs_p[i] > cutoffs_p[i + 1] for i in range(len(cutoffs_p) - 1))
    print(f"cutoff_decreases_with_information_prob: {is_decreasing}")
    print(f"substantial_unraveling_at_p_099: {cutoffs_p[-1] < 0.10}")

    # 2. Varying proprietary cost c with fixed information probability p = 0.70
    p_fixed = 0.70
    costs = [0.00, 0.05, 0.10, 0.20, 0.30]
    print("\nimpact_of_proprietary_cost (p = 0.70):")
    print(f"{'p (prob)':8s} | {'c (cost)':8s} | {'v* (cutoff)':11s} | {'P_silent':10s} | {'Fixed_pt_err':12s}")
    print("-" * 60)

    cutoffs_c: list[float] = []
    for c in costs:
        v_star, p_sil = solve_dye_cutoff(p_fixed, c)
        err = verify_fixed_point(v_star, p_fixed, c)
        cutoffs_c.append(v_star)
        print(f"{p_fixed:8.2f} | {c:8.2f} | {v_star:11.4f} | {p_sil:10.4f} | {err:12.2e}")

    print("-" * 60)
    is_increasing = all(cutoffs_c[i] < cutoffs_c[i + 1] for i in range(len(cutoffs_c) - 1))
    print(f"cutoff_increases_with_proprietary_cost: {is_increasing}")


main()
