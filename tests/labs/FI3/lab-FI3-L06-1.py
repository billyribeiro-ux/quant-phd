"""Lab FI3-L06-1: Adrian-Crump-Moench (ACM) linear regression term premium model.

SIMULATED: estimates the Adrian, Crump & Moench (2013) 3-step linear regression
affine term structure model and extracts model-based term premia.
Standard library and NumPy only; no network.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def estimate_acm(yields: np.ndarray, maturities: np.ndarray, num_factors: int = 3) -> dict[str, Any]:
    """Estimate ACM (2013) affine model via 3 OLS steps."""
    t_obs, k_mat = yields.shape

    # Step 1: PCA factors & VAR(1)
    y_mean = np.mean(yields, axis=0)
    y_c = yields - y_mean
    _, _, vt = np.linalg.svd(y_c, full_matrices=False)
    factors = y_c @ vt[:num_factors, :].T

    x_lag = np.column_stack([np.ones(t_obs - 1), factors[:-1]])
    x_lead = factors[1:]
    b_var, _, _, _ = np.linalg.lstsq(x_lag, x_lead, rcond=None)
    mu = b_var[0, :]
    phi = b_var[1:, :].T
    v_res = x_lead - x_lag @ b_var
    sigma_v = (v_res.T @ v_res) / float(len(v_res))

    # Step 2: Excess return regressions
    rx_mat = np.empty((t_obs - 1, k_mat - 1), dtype=np.float64)
    y1 = yields[:-1, 0]
    for k in range(1, k_mat):
        n = maturities[k]
        rx_mat[:, k - 1] = -(n - 1.0) * yields[1:, k - 1] + n * yields[:-1, k] - y1

    z_reg = np.column_stack([np.ones(t_obs - 1), v_res, factors[:-1]])
    coeffs, _, _, _ = np.linalg.lstsq(z_reg, rx_mat, rcond=None)
    alpha = coeffs[0, :]
    beta = coeffs[1 : 1 + num_factors, :].T
    c_mat = coeffs[1 + num_factors :, :].T
    res_e = rx_mat - z_reg @ coeffs
    sigma_e_sq = np.var(res_e, axis=0)

    # Step 3: Cross-sectional risk prices
    lambda1, _, _, _ = np.linalg.lstsq(beta, c_mat, rcond=None)
    alpha_adj = alpha + 0.5 * (np.sum((beta @ sigma_v) * beta, axis=1) + sigma_e_sq)
    lambda0, _, _, _ = np.linalg.lstsq(beta, alpha_adj, rcond=None)

    # Step 4: Expected short rates and term premium
    short_rate = yields[:, 0]
    w_sr = np.column_stack([np.ones(t_obs), factors])
    b_sr, _, _, _ = np.linalg.lstsq(w_sr, short_rate, rcond=None)
    delta0 = b_sr[0]
    delta1 = b_sr[1:]

    expected_short_rate = np.empty((t_obs, k_mat), dtype=np.float64)
    term_premium = np.empty((t_obs, k_mat), dtype=np.float64)

    for k in range(k_mat):
        n_steps = max(1, round(float(maturities[k])))
        e_factors = factors.copy()
        sum_r = delta0 + e_factors @ delta1
        for _ in range(1, n_steps):
            e_factors = mu + e_factors @ phi.T
            sum_r += delta0 + e_factors @ delta1
        avg_r = sum_r / float(n_steps)
        expected_short_rate[:, k] = avg_r
        term_premium[:, k] = yields[:, k] - avg_r

    return {
        "term_premium": term_premium,
        "expected_short_rate": expected_short_rate,
        "fitted_yields": yields.copy(),
        "phi": phi,
        "lambda1": lambda1,
        "lambda0": lambda0,
    }


def main() -> None:
    rng = np.random.default_rng(2013)
    t_obs = 100
    maturities = np.array([1.0, 2.0, 3.0, 5.0, 10.0], dtype=np.float64)

    # Persistent 3-factor yield dynamics (Level, Slope, Curvature)
    phi_diag = np.array([0.96, 0.84, 0.72])
    f = np.zeros((t_obs, 3), dtype=np.float64)
    f[0] = [0.045, -0.015, 0.005]
    for t in range(t_obs - 1):
        f[t + 1] = f[0] * (1.0 - phi_diag) + phi_diag * f[t] + rng.normal(0.0, [0.004, 0.005, 0.004])

    yields = np.zeros((t_obs, 5), dtype=np.float64)
    for i, m in enumerate(maturities):
        b = np.array([1.0, np.exp(-m / 3.0), (m / 3.0) * np.exp(-m / 3.0)])
        yields[:, i] = 0.015 + 0.004 * np.log(m) + f @ b

    acm = estimate_acm(yields, maturities, num_factors=3)
    tp = acm["term_premium"]
    esr = acm["expected_short_rate"]
    phi = acm["phi"]

    print("ACM (2013) Term-Structure Model Estimates:")
    print(f"  VAR(1) Phi matrix eigenvalues: {np.linalg.eigvals(phi).round(4)}")

    print("\nTerm Premium Decomposition at Final Observation (t = T):")
    for i, m in enumerate(maturities):
        print(
            f"  Maturity {m:4.1f}y: Yield = {yields[-1, i]:.4%}, "
            f"ExpShortRate = {esr[-1, i]:.4%}, "
            f"TermPremium = {tp[-1, i]:.4%} ({tp[-1, i] * 10000:6.1f} bps)"
        )

    # Verify articulation: term_premium + expected_short_rate == yields
    max_err = float(np.max(np.abs((tp + esr) - yields)))
    print(f"\nMaximum decomposition error |TP + ESR - Yield|: {max_err:.2e}")
    print(f"Exact articulation holds (error < 1e-12): {max_err < 1e-12}")


main()
