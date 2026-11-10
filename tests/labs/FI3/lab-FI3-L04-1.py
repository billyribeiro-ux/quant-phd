"""Lab FI3-L04-1: Fama-Bliss forward-rate regressions.

SIMULATED: generates synthetic zero-coupon yields and discrete forward rates to
estimate Fama-Bliss regressions for annual holding-period excess returns.
Standard library and NumPy only; no network.
"""

from __future__ import annotations

import numpy as np


def run_fama_bliss(yields: np.ndarray, maturities: np.ndarray) -> dict[int, tuple[float, float, float]]:
    """Run Fama-Bliss regressions:

    rx_{t+1}^{(n)} = alpha_n + beta_n * (f_t^{(n-1, n)} - y_t^{(1)}) + eps_{t+1}
    where rx_{t+1}^{(n)} = -(n-1)*y_{t+1}^{(n-1)} + n*y_t^{(n)} - y_t^{(1)}
    and f_t^{(n-1, n)} = n*y_t^{(n)} - (n-1)*y_t^{(n-1)}.
    Returns dict mapping maturity n to (alpha_n, beta_n, R^2).
    """
    t_obs, k_mat = yields.shape
    y1 = yields[:-1, 0]

    # Compute 1-year forward rates
    fwd = np.empty((t_obs - 1, k_mat), dtype=np.float64)
    fwd[:, 0] = y1
    for k in range(1, k_mat):
        n = maturities[k]
        n_prev = maturities[k - 1]
        fwd[:, k] = (n * yields[:-1, k] - n_prev * yields[:-1, k - 1]) / (n - n_prev)

    # Compute excess returns
    rx = np.empty((t_obs - 1, k_mat - 1), dtype=np.float64)
    for k in range(1, k_mat):
        n = maturities[k]
        rx[:, k - 1] = -(n - 1.0) * yields[1:, k - 1] + n * yields[:-1, k] - y1

    results: dict[int, tuple[float, float, float]] = {}
    for k in range(1, k_mat):
        n = round(maturities[k])
        fwd_spread = fwd[:, k] - y1
        design = np.column_stack([np.ones(t_obs - 1), fwd_spread])
        coeffs, _, _, _ = np.linalg.lstsq(design, rx[:, k - 1], rcond=None)
        alpha_n, beta_n = float(coeffs[0]), float(coeffs[1])

        fitted = design @ coeffs
        ss_tot = float(np.sum((rx[:, k - 1] - np.mean(rx[:, k - 1])) ** 2))
        ss_res = float(np.sum((rx[:, k - 1] - fitted) ** 2))
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

        results[n] = (alpha_n, beta_n, r2)

    return results


def main() -> None:
    rng = np.random.default_rng(777)
    t_obs = 120
    maturities = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)

    # Simulated yields where risk premium loads on the slope of the forward curve
    phi = 0.85
    f_slope = np.zeros(t_obs, dtype=np.float64)
    for t in range(t_obs - 1):
        f_slope[t + 1] = phi * f_slope[t] + rng.normal(0.0, 0.006)

    yields = np.zeros((t_obs, 5), dtype=np.float64)
    for i, m in enumerate(maturities):
        yields[:, i] = 0.04 + 0.005 * np.log(m) + (0.1 + 0.3 * m) * f_slope + rng.normal(0.0, 0.0005, size=t_obs)

    res = run_fama_bliss(yields, maturities)

    print("Fama-Bliss Regression Estimates (rx_{t+1}^{(n)} = alpha + beta * (f_t^{(n-1, n)} - y_t^{(1)}) + eps):")
    for n in sorted(res.keys()):
        alpha, beta, r2 = res[n]
        print(f"  Maturity n = {n}y: beta = {beta:6.4f}, alpha = {alpha:8.5f}, R^2 = {r2:6.4f}")

    # Check hypothesis: beta increases with maturity n
    betas = [res[n][1] for n in sorted(res.keys())]
    increases = all(betas[i] < betas[i + 1] for i in range(len(betas) - 1))
    print(f"\nFama-Bliss pattern: slope coefficients strictly increase with maturity: {increases}")
    print(f"Expectations hypothesis (beta = 0) rejected: {all(b > 0.5 for b in betas)}")


main()
