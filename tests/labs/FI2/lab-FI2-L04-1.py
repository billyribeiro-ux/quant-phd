"""Lab FI2-L04-1: Multi-factor Gaussian ATSM Riccati solver vs. numerical Runge-Kutta.

SIMULATED: solves the Duffie-Kan (1996) matrix Riccati ODE system for a 3-factor Gaussian
model (level, slope, curvature), comparing analytical closed-form factor loadings against
adaptive numerical integration across tenors from 3 months to 30 years.
"""

from __future__ import annotations

import numpy as np


def solve_riccati_analytical(
    tau_grid: np.ndarray,
    delta0: float,
    kappa: np.ndarray,
    sigma: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Analytical solution for diagonal Gaussian 3-factor Riccati system."""
    n_tenors = len(tau_grid)
    a_vec = np.zeros(n_tenors, dtype=np.float64)
    b_mat = np.zeros((n_tenors, 3), dtype=np.float64)

    for m, tm in enumerate(tau_grid):
        for i in range(3):
            ki = kappa[i]
            si = sigma[i]
            b_mat[m, i] = -(1.0 - np.exp(-ki * tm)) / ki
            int_b2 = (1.0 / (ki**2)) * (
                tm - 2.0 * (1.0 - np.exp(-ki * tm)) / ki + (1.0 - np.exp(-2.0 * ki * tm)) / (2.0 * ki)
            )
            a_vec[m] += 0.5 * (si**2) * int_b2
        a_vec[m] -= delta0 * tm

    return a_vec, b_mat


def solve_riccati_rk4(
    tau_grid: np.ndarray,
    delta0: float,
    kappa: np.ndarray,
    sigma: np.ndarray,
    n_substeps: int = 500,
) -> tuple[np.ndarray, np.ndarray]:
    """Solve Riccati ODE system by 4th-order Runge-Kutta numerical integration."""
    n_tenors = len(tau_grid)
    a_rk = np.zeros(n_tenors, dtype=np.float64)
    b_rk = np.zeros((n_tenors, 3), dtype=np.float64)

    k_diag = kappa
    sig_sq = sigma**2

    # Integrate sequentially from 0 through tau_grid
    curr_tau = 0.0
    curr_a = 0.0
    curr_b = np.zeros(3, dtype=np.float64)

    def rhs(b: np.ndarray) -> tuple[float, np.ndarray]:
        # dB/dtau = -K^T B - 1
        db = -k_diag * b - 1.0
        # dA/dtau = -delta0 + 0.5 * B^T Sigma Sigma^T B
        da = -delta0 + 0.5 * float(np.sum(sig_sq * (b**2)))
        return da, db

    for m, target_tau in enumerate(tau_grid):
        h = (target_tau - curr_tau) / n_substeps
        for _ in range(n_substeps):
            k1_a, k1_b = rhs(curr_b)
            k2_a, k2_b = rhs(curr_b + 0.5 * h * k1_b)
            k3_a, k3_b = rhs(curr_b + 0.5 * h * k2_b)
            k4_a, k4_b = rhs(curr_b + h * k3_b)

            curr_b += (h / 6.0) * (k1_b + 2.0 * k2_b + 2.0 * k3_b + k4_b)
            curr_a += (h / 6.0) * (k1_a + 2.0 * k2_a + 2.0 * k3_a + k4_a)

        curr_tau = target_tau
        a_rk[m] = curr_a
        b_rk[m, :] = curr_b

    return a_rk, b_rk


def main() -> None:
    # 3-factor Gaussian ATSM (Dai & Singleton 2000 A_0(3) canonical model)
    delta0 = 0.028  # 2.80% short-rate intercept
    kappa = np.array([0.05, 0.25, 0.85], dtype=np.float64)  # Level, Slope, Curvature
    sigma = np.array([0.012, 0.016, 0.022], dtype=np.float64)

    tenors = np.array([0.25, 1.0, 2.0, 5.0, 10.0, 30.0], dtype=np.float64)

    a_exact, b_exact = solve_riccati_analytical(tenors, delta0, kappa, sigma)
    a_rk, b_rk = solve_riccati_rk4(tenors, delta0, kappa, sigma)

    # Convert to yield loadings: y(tau) = -A/tau - B/tau * X_t
    a_yield_exact = -a_exact / tenors
    h_yield_exact = -b_exact / tenors[:, np.newaxis]

    a_yield_rk = -a_rk / tenors
    h_yield_rk = -b_rk / tenors[:, np.newaxis]

    print("SIMULATED 3-Factor Gaussian ATSM: Analytical vs. Runge-Kutta 4:")
    print(f"  Params: delta0 = {delta0:.4f}, kappa = {kappa.tolist()}, sigma = {sigma.tolist()}")
    print("Tenor | a_exact |  a_RK4  | H1_exact | H1_RK4  | H2_exact | H2_RK4  | H3_exact | H3_RK4")
    print("-" * 88)

    for m, t in enumerate(tenors):
        print(
            f" {t:5.2f}| {a_yield_exact[m]:.5f} | {a_yield_rk[m]:.5f} | "
            f"{h_yield_exact[m, 0]:.5f}  | {h_yield_rk[m, 0]:.5f} | "
            f"{h_yield_exact[m, 1]:.5f}  | {h_yield_rk[m, 1]:.5f} | "
            f"{h_yield_exact[m, 2]:.5f}  | {h_yield_rk[m, 2]:.5f}"
        )

    max_a_diff = np.max(np.abs(a_exact - a_rk))
    max_b_diff = np.max(np.abs(b_exact - b_rk))
    print(f"\nMaximum Riccati differences across all tenors: A_err = {max_a_diff:.2e}, B_err = {max_b_diff:.2e}")


main()
