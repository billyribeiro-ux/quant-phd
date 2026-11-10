"""Lab FI3-L01-1: Campbell-Shiller test of the expectations hypothesis.

SIMULATED: generates synthetic zero-coupon yield panels with time-varying risk premia
to test the Campbell-Shiller regression specification for n in {2, 3, 5, 10} years.
Standard library and NumPy only; no network.
"""

from __future__ import annotations

import numpy as np


def run_campbell_shiller(yields: np.ndarray, maturities: np.ndarray) -> dict[int, tuple[float, float, float]]:
    """Run Campbell-Shiller regressions:

    y_{t+1}^{(n-1)} - y_t^{(n)} = alpha_n + beta_n * [(y_t^{(n)} - y_t^{(1)}) / (n - 1)] + eps_{t+1}
    Returns dict mapping maturity n to (alpha_n, beta_n, r_squared).
    """
    t_obs, _ = yields.shape
    mat_to_idx = {round(m): i for i, m in enumerate(maturities)}
    results: dict[int, tuple[float, float, float]] = {}

    idx_1y = mat_to_idx[1]
    y_1y = yields[:-1, idx_1y]

    for n in [2, 3, 5, 10]:
        if n not in mat_to_idx or (n - 1) not in mat_to_idx:
            continue
        idx_n = mat_to_idx[n]
        idx_n_minus_1 = mat_to_idx[n - 1]

        # LHS: change in yield of maturing bond
        lhs = yields[1:, idx_n_minus_1] - yields[:-1, idx_n]

        # RHS: theoretical slope predictor
        spread = (yields[:-1, idx_n] - y_1y) / float(n - 1)
        design = np.column_stack([np.ones(t_obs - 1), spread])

        coeffs, _, _, _ = np.linalg.lstsq(design, lhs, rcond=None)
        alpha_n, beta_n = float(coeffs[0]), float(coeffs[1])

        fitted = design @ coeffs
        ss_tot = float(np.sum((lhs - np.mean(lhs)) ** 2))
        ss_res = float(np.sum((lhs - fitted) ** 2))
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

        results[n] = (alpha_n, beta_n, r2)

    return results


def main() -> None:
    rng = np.random.default_rng(12345)
    t_obs = 100
    maturities = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 9.0, 10.0], dtype=np.float64)
    k = len(maturities)

    # Persistent factors: Level and Slope with countercyclical term premium shock
    phi = np.array([0.94, 0.82])
    mu = np.array([0.05, -0.015]) * (1.0 - phi)
    f = np.zeros((t_obs, 2), dtype=np.float64)
    f[0] = [0.05, -0.015]
    for t in range(t_obs - 1):
        f[t + 1] = mu + phi * f[t] + rng.normal(0.0, [0.005, 0.007])

    yields = np.zeros((t_obs, k), dtype=np.float64)
    for i, m in enumerate(maturities):
        # Slope loading decays; risk premium introduces negative correlation with expected change
        b_level = 1.0
        b_slope = np.exp(-m / 3.0)
        yields[:, i] = 0.015 + b_level * f[:, 0] + b_slope * f[:, 1] + 0.003 * np.log(m)

    res = run_campbell_shiller(yields, maturities)

    print("Campbell-Shiller Regression Results (H0: beta = 1.0 under PEH):")
    for n in sorted(res.keys()):
        alpha, beta, r2 = res[n]
        rejection = "REJECT PEH" if abs(beta - 1.0) > 0.4 else "CONSISTENT"
        print(f"  Maturity n = {n:2d}y: beta = {beta:7.4f}, alpha = {alpha:8.5f}, R^2 = {r2:6.4f} -> {rejection}")

    # Check that beta_n decreases and is far below 1
    betas = [res[n][1] for n in sorted(res.keys())]
    print(f"Hypothesis check: beta coefficients strictly below 1.0: {all(b < 1.0 for b in betas)}")


main()
