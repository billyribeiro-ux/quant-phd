"""Lab FI2-project-2: Factor loadings and Kalman innovation engine (Rung 2 completion).

Solution twin for the Rung 2 completion problem: implements the analytical
Riccati factor loadings, evaluates measurement innovations, and computes
yield pricing RMSE in basis points.
"""

from __future__ import annotations

import numpy as np


def compute_loadings_and_innovations(
    tau: np.ndarray,
    delta0: float,
    kappa: np.ndarray,
    sigma: np.ndarray,
    x_pred: np.ndarray,
    observed_yields: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    """Compute Riccati factor loadings, measurement predictions, innovations, and RMSE."""
    n_maturities = len(tau)
    b_mat = np.zeros((n_maturities, 3), dtype=np.float64)
    a_vec = np.zeros(n_maturities, dtype=np.float64)

    for m in range(n_maturities):
        tm = float(tau[m])
        for i in range(3):
            ki = float(kappa[i])
            si = float(sigma[i])
            # Blank 1 in completion problem: Riccati factor loading B_i(tau)
            b_mat[m, i] = -(1.0 - np.exp(-ki * tm)) / ki

            int_b2 = (1.0 / (ki**2)) * (
                tm - 2.0 * (1.0 - np.exp(-ki * tm)) / ki + (1.0 - np.exp(-2.0 * ki * tm)) / (2.0 * ki)
            )
            a_vec[m] += 0.5 * (si**2) * int_b2
        a_vec[m] -= delta0 * tm

    a_yield = -a_vec / tau
    h_yield = -b_mat / tau[:, np.newaxis]

    # Blank 2 in completion problem: Predicted yields and innovations
    predicted_yields = a_yield + h_yield @ x_pred
    innovations = observed_yields - predicted_yields

    # Blank 3 in completion problem: Pricing RMSE in basis points
    rmse_bps = float(np.sqrt(np.mean(innovations**2)) * 10_000.0)

    return a_yield, h_yield, innovations, rmse_bps


def main() -> None:
    # SIMULATED snapshot test
    tau = np.array([0.5, 1.0, 2.0, 5.0, 10.0], dtype=np.float64)
    delta0 = 0.025
    kappa = np.array([0.06, 0.25, 0.85], dtype=np.float64)
    sigma = np.array([0.010, 0.014, 0.018], dtype=np.float64)

    x_pred = np.array([0.012, -0.005, 0.003], dtype=np.float64)
    # Observed yields matching model plus 4 bps noise
    a_true, h_true, _, _ = compute_loadings_and_innovations(
        tau, delta0, kappa, sigma, x_pred, np.zeros(len(tau), dtype=np.float64)
    )
    observed_yields = a_true + h_true @ x_pred + np.array([0.0003, -0.0004, 0.0002, 0.0005, -0.0003])

    a_yield, _h_yield, innovations, rmse_bps = compute_loadings_and_innovations(
        tau, delta0, kappa, sigma, x_pred, observed_yields
    )

    print("Completed Factor Loadings & Innovation Analysis (SIMULATED Rung 2):")
    print(f"  Maturities evaluated: {tau.tolist()} years")
    print(f"  Short-rate baseline a(tau): {[round(float(a), 4) for a in a_yield]}")
    print(f"  Pricing innovations (bps): {[round(float(v) * 10_000, 2) for v in innovations]}")
    print(f"  Snapshot pricing RMSE: {rmse_bps:.2f} bps")


main()
