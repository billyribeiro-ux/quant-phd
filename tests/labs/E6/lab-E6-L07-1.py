"""Lab E6-L07-1: Determinacy, root counting, and the Taylor principle.

Constructs the dynamic companion matrix for the three-equation New Keynesian system
across a parameter grid for (phi_pi, phi_y). Computes system eigenvalues and tests whether
both roots lie outside the unit circle in the complex plane, matching the analytical
generalized Taylor principle condition: kappa * (phi_pi - 1) + (1 - beta) * phi_y > 0.
"""

from __future__ import annotations

import numpy as np


def analyze_determinacy(
    beta: float, sigma: float, kappa: float, phi_pi: float, phi_y: float
) -> tuple[bool, bool, float, float]:
    """Compute eigenvalues and check determinacy conditions."""
    # System companion matrix M for [E_t[x_{t+1}], E_t[pi_{t+1}]]^T = M * [x_t, pi_t]^T
    m_mat = np.array(
        [
            [1.0 + phi_y / sigma + kappa / (beta * sigma), (phi_pi - 1.0 / beta) / sigma],
            [-kappa / beta, 1.0 / beta],
        ],
        dtype=np.float64,
    )
    eigenvalues = np.linalg.eigvals(m_mat)
    moduli = np.abs(eigenvalues)

    # Determinacy requires all non-predetermined roots outside the unit circle (|lambda| > 1)
    roots_outside = bool(np.all(moduli > 1.0 + 1e-10))

    # Analytical generalized Taylor principle
    det_metric = kappa * (phi_pi - 1.0) + (1.0 - beta) * phi_y
    analytical_cond = bool(det_metric > 1e-10)

    return roots_outside, analytical_cond, float(moduli[0]), float(moduli[1])


def main() -> None:
    beta = 0.99
    sigma = 1.0
    kappa = 0.1

    print("Determinacy and Taylor Principle Analysis (beta=0.99, sigma=1.0, kappa=0.1):")
    print("  Critical boundary: phi_pi = 1.0 - (1 - beta) * phi_y / kappa = 1.0 - 0.1 * phi_y\n")

    phi_y_grid = [0.0, 0.5, 1.0]
    for phi_y in phi_y_grid:
        crit_phi_pi = 1.0 - (1.0 - beta) * phi_y / kappa
        test_points = [
            (crit_phi_pi - 0.2, "Indeterminate"),
            (crit_phi_pi, "Boundary (Unit Root)"),
            (crit_phi_pi + 0.2, "Determinate"),
        ]

        print(f"--- phi_y = {phi_y:.1f} (Critical phi_pi = {crit_phi_pi:.4f}) ---")
        for phi_pi, regime in test_points:
            roots_out, cond_holds, mod1, mod2 = analyze_determinacy(beta, sigma, kappa, phi_pi, phi_y)
            agreement = roots_out == cond_holds
            print(
                f"  phi_pi = {phi_pi:6.4f} [{regime:21s}] | "
                f"|lambda_1| = {mod1:6.4f}, |lambda_2| = {mod2:6.4f} | "
                f"Determinate: {roots_out!s:5s} | Agreement: {agreement!s}"
            )


main()
