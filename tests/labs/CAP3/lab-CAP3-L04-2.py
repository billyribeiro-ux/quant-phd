"""Lab CAP3-L04-2: Field Prelim III, Problem B: New Keynesian Determinacy.

Evaluates the Blanchard-Kahn conditions and Taylor principle determinacy
for the canonical 3-equation New Keynesian general equilibrium model.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def check_new_keynesian_determinacy(
    beta: float,
    sigma: float,
    kappa: float,
    phi_pi: float,
    phi_y: float,
) -> tuple[bool, float, np.ndarray]:
    """Evaluate determinacy criterion: phi_pi + ((1 - beta)/kappa) * phi_y > 1.0."""
    taylor_criterion = phi_pi + ((1.0 - beta) / kappa) * phi_y

    # Matrix form of the expectations system [y_t, pi_t]' = A * E_t[y_{t+1}, pi_{t+1}]'
    # Derived from:
    # y_t = E_t[y_{t+1}] - (1/sigma)(phi_pi * pi_t + phi_y * y_t - E_t[pi_{t+1}])
    # pi_t = beta * E_t[pi_{t+1}] + kappa * y_t
    # Invert to state-space system matrix A
    denom = 1.0 + (1.0 / sigma) * phi_y + (kappa / sigma) * phi_pi
    a11 = (1.0 + (kappa / sigma) * phi_pi * beta) / denom
    a12 = (1.0 / sigma) * (1.0 - beta * phi_pi) / denom
    a21 = kappa / denom
    a22 = (beta * (1.0 + (1.0 / sigma) * phi_y) + (kappa / sigma)) / denom
    a_mat = np.array([[a11, a12], [a21, a22]])

    eigenvalues = np.linalg.eigvals(a_mat)
    # Both variables are forward-looking jump variables; determinacy requires
    # both eigenvalues of the expectations matrix to lie strictly inside the unit circle
    moduli = np.abs(eigenvalues)
    is_determinate = bool(np.all(moduli < 1.0) and taylor_criterion > 1.0)
    return is_determinate, taylor_criterion, eigenvalues


def main() -> None:
    beta = 0.99
    sigma = 1.0
    kappa = 0.15

    regimes: list[dict[str, Any]] = [
        {"name": "Aggressive Inflation Targeting", "phi_pi": 1.5, "phi_y": 0.5},
        {"name": "Pure Inflation Targeting", "phi_pi": 1.1, "phi_y": 0.0},
        {"name": "Weak Monetary Response (Passive)", "phi_pi": 0.8, "phi_y": 0.2},
        {"name": "Boundary Indeterminate Case", "phi_pi": 0.9, "phi_y": 1.5},
    ]

    print("--- New Keynesian System Determinacy & Blanchard-Kahn Check ---")
    for r in regimes:
        p_pi = float(r["phi_pi"])
        p_y = float(r["phi_y"])
        determinate, crit, eigs = check_new_keynesian_determinacy(beta, sigma, kappa, p_pi, p_y)
        status = "UNIQUE STABLE (Determinate)" if determinate else "INDETERMINATE / SUNSPOT"
        mod_str = f"[{abs(eigs[0]):.4f}, {abs(eigs[1]):.4f}]"
        print(
            f"{r['name']}: phi_pi={p_pi:.1f}, phi_y={p_y:.1f} | Criterion: {crit:.4f} | Moduli: {mod_str} -> {status}"
        )


main()
