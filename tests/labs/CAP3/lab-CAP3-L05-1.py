"""Lab CAP3-L05-1: Macro-Finance Affine Term Structure No-Arbitrage SDF Estimation.

Estimates the cross-field pricing kernel connecting monetary policy rates,
macroeconomic output gaps, and the term structure of bond yields.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # 2-factor macro-finance state vector X_t = [inflation_gap, output_gap]'
    np.random.seed(303)

    # Physical VAR(1) dynamics: X_{t+1} = mu + Phi * X_t + v_{t+1}
    phi_mat = np.array([[0.75, 0.10], [0.05, 0.85]])
    sigma_v = np.array([[0.0004, 0.0001], [0.0001, 0.0009]])
    chol_v = np.linalg.cholesky(sigma_v)

    # Affine short rate: r_t = delta_0 + delta_1' X_t
    delta_0 = 0.025
    delta_1 = np.array([0.65, 0.40])

    # Market prices of risk: lambda_t = lambda_0 + lambda_1 * X_t
    lambda_0 = np.array([-0.15, -0.25])

    # Recursive affine yield coefficients: A_n, B_n for n = 1, 4, 12 quarters
    # p_t^(n) = -A_n - B_n' X_t, y_t^(n) = (A_n + B_n' X_t) / n
    maturities = [1, 4, 12]
    yield_intercepts = []
    yield_loadings = []

    a_curr = 0.0
    b_curr = np.zeros(2)

    for n in range(1, max(maturities) + 1):
        # Recursion:
        # A_{n+1} = A_n + B_n' (mu - sigma_v lambda_0) - 0.5 * B_n' sigma_v B_n + delta_0
        # B_{n+1} = (Phi - sigma_v lambda_1)' B_n + delta_1
        # For simple homoskedastic model with lambda_1 = 0:
        a_next = a_curr - float(b_curr @ (chol_v @ lambda_0)) - 0.5 * float(b_curr @ sigma_v @ b_curr) + delta_0
        b_next = phi_mat.T @ b_curr + delta_1
        a_curr, b_curr = a_next, b_next
        if n in maturities:
            yield_intercepts.append(a_curr / float(n))
            yield_loadings.append(b_curr / float(n))

    print("--- Macro-Finance No-Arbitrage Term Structure Calibration ---")
    for idx, mat in enumerate(maturities):
        int_val = yield_intercepts[idx] * 100.0
        b_val = yield_loadings[idx]
        print(
            f"Maturity {mat:02d}Q: Yield Intercept = {int_val:.2f}% | "
            f"Loadings (pi, y) = [{b_val[0]:.4f}, {b_val[1]:.4f}]"
        )


main()
