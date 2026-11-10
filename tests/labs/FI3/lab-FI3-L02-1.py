"""Lab FI3-L02-1: Excess bond return dynamics and covariance structure.

SIMULATED: generates synthetic zero-coupon yield panels to compute 1-year holding
period excess log returns across annual maturities 2 through 5.
Standard library and NumPy only; no network.
"""

from __future__ import annotations

import numpy as np


def compute_excess_returns(yields: np.ndarray, maturities: np.ndarray) -> np.ndarray:
    """Compute 1-year holding period excess log returns:

    rx_{t+1}^{(n)} = -(n-1)*y_{t+1}^{(n-1)} + n*y_t^{(n)} - y_t^{(1)}
    for n = 2, ..., K.
    """
    t_obs, k_mat = yields.shape
    rx = np.empty((t_obs - 1, k_mat - 1), dtype=np.float64)
    for n_idx in range(1, k_mat):
        n_val = maturities[n_idx]
        rx[:, n_idx - 1] = -(n_val - 1.0) * yields[1:, n_idx - 1] + n_val * yields[:-1, n_idx] - yields[:-1, 0]
    return rx


def main() -> None:
    rng = np.random.default_rng(42)
    t_obs = 80
    maturities = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)

    # Simulated yields driven by persistent level and slope factors
    phi_l, phi_s = 0.95, 0.82
    level = np.zeros(t_obs, dtype=np.float64)
    slope = np.zeros(t_obs, dtype=np.float64)
    level[0] = 0.045
    slope[0] = -0.015

    for t in range(t_obs - 1):
        level[t + 1] = 0.045 * (1.0 - phi_l) + phi_l * level[t] + rng.normal(0.0, 0.006)
        slope[t + 1] = -0.015 * (1.0 - phi_s) + phi_s * slope[t] + rng.normal(0.0, 0.005)

    yields = np.zeros((t_obs, 5), dtype=np.float64)
    for i, m in enumerate(maturities):
        b_slope = np.exp(-m / 2.5)
        yields[:, i] = level + b_slope * slope + 0.005 * np.log(m) + rng.normal(0.0, 0.0003, size=t_obs)

    rx = compute_excess_returns(yields, maturities)

    means = np.mean(rx, axis=0)
    stds = np.std(rx, axis=0)
    corr = np.corrcoef(rx, rowvar=False)

    print("Excess Bond Returns (Annual Holding Period, n = 2..5):")
    for i, m in enumerate([2, 3, 4, 5]):
        print(f"  Maturity n = {m}y: mean = {means[i]:.4%}, std = {stds[i]:.4%}, Sharpe = {means[i] / stds[i]:.4f}")

    print("\nCorrelation Matrix of Excess Returns:")
    for row in corr:
        print("  " + "  ".join(f"{val:6.4f}" for val in row))

    min_corr = float(np.min(corr))
    is_monotonic_std = all(stds[i] < stds[i + 1] for i in range(len(stds) - 1))
    print(f"\nMinimum pairwise correlation: {min_corr:.4f} (> 0.85: {min_corr > 0.85})")
    print(f"Standard deviation scales monotonically with maturity: {is_monotonic_std}")


main()
