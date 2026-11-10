"""Lab E6-project-2: Completion problem solution twin for New Keynesian model solver.

Full working solution for Rung 2 completion problem.
Model output, no data.
"""

from __future__ import annotations


def solve_nk_completion(
    beta: float, sigma: float, kappa: float, phi_pi: float, phi_y: float, rho: float
) -> tuple[bool, float, float]:
    # Check determinacy condition via the generalized Taylor principle
    is_det = (kappa * (phi_pi - 1.0) + (1.0 - beta) * phi_y) > 0.0

    if not is_det:
        raise ValueError("Indeterminate equilibrium")

    # Solve for undetermined coefficients
    delta = (1.0 - beta * rho) * (sigma * (1.0 - rho) + phi_y) + kappa * (phi_pi - rho)
    b = (1.0 - beta * rho) / delta
    a = kappa / delta

    return is_det, b, a


def main() -> None:
    beta = 0.99
    sigma = 1.0
    kappa = 0.12
    phi_pi = 1.5
    phi_y = 0.5
    rho = 0.6

    is_det, b, a = solve_nk_completion(beta, sigma, kappa, phi_pi, phi_y, rho)

    print("Rung 2 Completion Problem Check:")
    print(f"  Determinacy verified: {is_det}")
    print(f"  Output gap coefficient b: {b:.6f}")
    print(f"  Inflation coefficient a:  {a:.6f}")


main()
