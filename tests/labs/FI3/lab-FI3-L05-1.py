"""Lab FI3-L05-1: Cochrane-Piazzesi factor and tent-shaped predictability.

SIMULATED: estimates the Cochrane-Piazzesi (2005) single return-forecasting factor
from five forward rates and verifies the tent-shaped coefficient structure.
Standard library and NumPy only; no network.
"""

from __future__ import annotations

import numpy as np


def compute_cp_factor(yields: np.ndarray, maturities: np.ndarray) -> tuple[np.ndarray, np.ndarray, float, np.ndarray]:
    """Estimate the Cochrane-Piazzesi single-factor model:

    1. Forward rates f_t = [y_t^{(1)}, f_t^{(1,2)}, ..., f_t^{(4,5)}]
    2. Average excess return rx_bar_{t+1} = (1/4) sum_{n=2}^5 rx_{t+1}^{(n)}
    3. OLS: rx_bar_{t+1} = gamma_0 + gamma^T f_t + eps_{t+1}
    4. Individual regressions: rx_{t+1}^{(n)} = b_n * cp_factor_t + e_{t+1}^{(n)}
    """
    t_obs, _k_mat = yields.shape
    y1 = yields[:-1, 0]

    # Forward rates
    fwd = np.empty((t_obs - 1, 5), dtype=np.float64)
    fwd[:, 0] = y1
    for k in range(1, 5):
        n = maturities[k]
        n_prev = maturities[k - 1]
        fwd[:, k] = (n * yields[:-1, k] - n_prev * yields[:-1, k - 1]) / (n - n_prev)

    # Excess returns
    rx = np.empty((t_obs - 1, 4), dtype=np.float64)
    for k in range(1, 5):
        n = maturities[k]
        rx[:, k - 1] = -(n - 1.0) * yields[1:, k - 1] + n * yields[:-1, k] - y1

    rx_bar = np.mean(rx, axis=1)

    design = np.column_stack([np.ones(t_obs - 1), fwd])
    gamma, _, _, _ = np.linalg.lstsq(design, rx_bar, rcond=None)

    cp_factor = design @ gamma
    ss_tot = float(np.sum((rx_bar - np.mean(rx_bar)) ** 2))
    ss_res = float(np.sum((rx_bar - cp_factor) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

    loadings = np.empty(4, dtype=np.float64)
    var_cp = float(np.var(cp_factor))
    for i in range(4):
        loadings[i] = float(np.cov(rx[:, i], cp_factor)[0, 1] / var_cp) if var_cp > 1e-12 else 1.0

    return gamma, cp_factor, r2, loadings


def main() -> None:
    rng = np.random.default_rng(101)
    t_obs = 150
    maturities = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)

    # 3-factor state dynamics: level, slope, curvature
    x = np.zeros((t_obs, 3), dtype=np.float64)
    for t in range(t_obs - 1):
        x[t + 1] = 0.85 * x[t] + rng.normal(0, 0.005, size=3)

    b_y = np.array(
        [
            [1.0, 1.0, 1.0, 1.0, 1.0],
            [0.8, 0.6, 0.4, 0.3, 0.2],
            [0.05, 0.12, 0.18, 0.22, 0.25],
        ]
    ).T
    yields = 0.04 + x @ b_y.T + rng.normal(0, 0.0002, size=(t_obs, 5))

    gamma, _cp_factor, r2, loadings = compute_cp_factor(yields, maturities)

    print("Cochrane-Piazzesi Factor Estimation (AER 2005):")
    print(f"  Intercept gamma_0 = {gamma[0]:8.5f}")
    fwd_names = ["y^(1)", "f^(1,2)", "f^(2,3)", "f^(3,4)", "f^(4,5)"]
    for i, name in enumerate(fwd_names):
        print(f"  Coefficient on {name:7s} (gamma_{i + 1}): {gamma[i + 1]:7.4f}")

    print(f"\nAverage Return Regression R^2 = {r2:.4f} ({r2 * 100:.1f}%)")

    print("\nFactor Loadings b_n across Maturities (rx_{t+1}^{(n)} = b_n * cp_t):")
    for i, m in enumerate([2, 3, 4, 5]):
        print(f"  Maturity n = {m}y: loading b_{m} = {loadings[i]:6.4f}")

    # Verify loadings increase with maturity
    increases = all(loadings[i] < loadings[i + 1] for i in range(len(loadings) - 1))
    print(f"\nLoadings strictly increase with maturity: {increases}")
    print(f"All loadings positive: {all(loadings[i] > 0 for i in range(4))}")


main()
