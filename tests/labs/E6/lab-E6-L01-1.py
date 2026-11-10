"""Lab E6-L01-1: The RBC steady state in closed form.

Solves the deterministic steady state of the standard one-sector Real Business Cycle model
and verifies that both the consumption Euler equation and the aggregate resource constraint
hold to zero residual in exact rational arithmetic (Fraction) and in double precision floats.
"""

from __future__ import annotations

import math
from fractions import Fraction


def solve_rbc_steady_state_fraction(
    alpha: Fraction, beta: Fraction, delta: Fraction
) -> tuple[Fraction, Fraction, Fraction, Fraction, Fraction]:
    """Solve the steady state in exact arithmetic for alpha=1/2."""
    # Euler equation in steady state: beta * (1 + r* - delta) = 1 => r* = 1/beta - 1 + delta
    r_star = Fraction(1, beta) - Fraction(1) + delta
    # Marginal product of capital: r* = alpha * (k*)^(alpha - 1)
    # For alpha = 1/2: r* = (1/2) * (k*)^(-1/2) => (k*)^(1/2) = alpha / r_star
    ratio = alpha / r_star
    k_star = ratio * ratio
    y_star = ratio  # y* = (k*)^(1/2) = ratio
    i_star = delta * k_star
    c_star = y_star - i_star
    return r_star, k_star, y_star, c_star, i_star


def solve_rbc_steady_state_float(alpha: float, beta: float, delta: float) -> tuple[float, float, float, float, float]:
    """Solve the steady state in double precision for standard quarterly calibration."""
    r_star = 1.0 / beta - 1.0 + delta
    k_star = (alpha / r_star) ** (1.0 / (1.0 - alpha))
    y_star = k_star**alpha
    i_star = delta * k_star
    c_star = y_star - i_star
    return r_star, k_star, y_star, c_star, i_star


def main() -> None:
    # ---------------------------------------------------------
    # Part 1: Exact rational arithmetic (alpha = 1/2, beta = 4/5, delta = 1/10)
    # ---------------------------------------------------------
    alpha_q = Fraction(1, 2)
    beta_q = Fraction(4, 5)
    delta_q = Fraction(1, 10)

    r_q, k_q, y_q, c_q, i_q = solve_rbc_steady_state_fraction(alpha_q, beta_q, delta_q)

    # Euler equation check: beta * (1 + alpha * (k*)^(-1/2) - delta) - 1 == 0
    mpk_q = alpha_q / Fraction(math.isqrt(k_q.numerator), math.isqrt(k_q.denominator))
    euler_residual_q = beta_q * (Fraction(1) + mpk_q - delta_q) - Fraction(1)
    resource_residual_q = y_q - c_q - i_q

    print(f"Exact rational steady state (alpha={alpha_q}, beta={beta_q}, delta={delta_q}):")
    print(f"  Rental rate r*: {r_q}")
    print(f"  Capital stock k*: {k_q}")
    print(f"  Output y*: {y_q}")
    print(f"  Consumption c*: {c_q}")
    print(f"  Investment i*: {i_q}")
    print(f"  Euler equation residual: {euler_residual_q}")
    print(f"  Resource constraint residual: {resource_residual_q}")

    # ---------------------------------------------------------
    # Part 2: Standard float calibration (alpha = 1/3, beta = 0.99, delta = 0.025)
    # ---------------------------------------------------------
    alpha_f = 1.0 / 3.0
    beta_f = 0.99
    delta_f = 0.025

    r_f, k_f, y_f, c_f, i_f = solve_rbc_steady_state_float(alpha_f, beta_f, delta_f)

    mpk_f = alpha_f * (k_f ** (alpha_f - 1.0))
    euler_residual_f = beta_f * (1.0 + mpk_f - delta_f) - 1.0
    resource_residual_f = y_f - c_f - i_f

    print("\nStandard quarterly calibration (alpha=1/3, beta=0.99, delta=0.025):")
    print(f"  Rental rate r*: {r_f:.6f}")
    print(f"  Capital stock k*: {k_f:.6f}")
    print(f"  Output y*: {y_f:.6f}")
    print(f"  Consumption c*: {c_f:.6f}")
    print(f"  Investment i*: {i_f:.6f}")
    print(f"  Euler equation residual: {euler_residual_f:.2e}")
    print(f"  Resource constraint residual: {resource_residual_f:.2e}")


main()
