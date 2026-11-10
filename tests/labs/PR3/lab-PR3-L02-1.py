"""Lab PR3-L02-1: Continuous-Time Multi-Asset Growth-Optimal Portfolio and Numeraire Property.

SIMULATED: Verification of multi-asset GOP weights, growth rate, and numeraire martingale property.
"""

from __future__ import annotations

import numpy as np


def compute_gop(mu: np.ndarray, r: float, cov: np.ndarray) -> tuple[np.ndarray, float, float]:
    """Compute continuous multi-asset Growth-Optimal Portfolio weights, Sharpe, and growth rate."""
    excess_mu = mu - r
    w_star = np.linalg.solve(cov, excess_mu)
    port_var = float(w_star @ cov @ w_star)
    port_excess = float(w_star @ excess_mu)
    sharpe = float(np.sqrt(port_excess))
    # Growth rate: r + w*' excess_mu - 0.5 * w*' cov * w*
    growth = float(r + port_excess - 0.5 * port_var)
    return w_star, sharpe, growth


def verify_numeraire_property(
    mu: np.ndarray,
    r: float,
    cov: np.ndarray,
    t_horizon: float = 1.0,
    n_paths: int = 20000,
    seed: int = 42,
) -> np.ndarray:
    """Verify in Monte Carlo that S_i(t) / W*(t) is a martingale with expectation 1.0."""
    rng = np.random.default_rng(seed)
    n_assets = len(mu)
    w_star, _, g_star = compute_gop(mu, r, cov)

    # Cholesky factor for asset returns: dS_i / S_i = mu_i dt + sigma_i dW
    chol = np.linalg.cholesky(cov)
    z = rng.standard_normal((n_paths, n_assets))
    diff = z @ chol.T * np.sqrt(t_horizon)

    # Asset prices at t_horizon: S_i(T) = S_i(0) * exp((mu_i - 0.5 * sigma_i^2) * T + diff_i)
    asset_vars = np.diag(cov)
    log_s = (mu - 0.5 * asset_vars) * t_horizon + diff
    s_t = np.exp(log_s)

    # GOP portfolio wealth at t_horizon:
    # dW* / W* = (r + w*' excess_mu) dt + w*' chol dW
    port_vol_shock = diff @ w_star
    log_w_star = g_star * t_horizon + port_vol_shock
    w_star_t = np.exp(log_w_star)

    # Deflated price: (S_i(t) / S_i(0)) / (W*(t) / W*(0))
    deflated = s_t / w_star_t[:, np.newaxis]
    expected_deflated = np.mean(deflated, axis=0)
    return np.asarray(expected_deflated, dtype=np.float64)


def main() -> None:
    r = 0.03
    mu = np.array([0.08, 0.10, 0.12], dtype=np.float64)
    cov = np.array(
        [
            [0.0400, 0.0120, 0.0080],
            [0.0120, 0.0625, 0.0150],
            [0.0080, 0.0150, 0.0900],
        ],
        dtype=np.float64,
    )

    w_star, sharpe, g_star = compute_gop(mu, r, cov)
    deflated_means = verify_numeraire_property(mu, r, cov, t_horizon=1.0, n_paths=20000, seed=42)

    print("Multi-Asset Growth-Optimal Portfolio (GOP):")
    print(f"Risk-free rate: {r:.4f}")
    print(f"Asset Expected Returns: {mu}")
    print(f"GOP Optimal Weights w*: {np.round(w_star, 4)}")
    print(f"Total Leverage sum(w*): {float(np.sum(w_star)):.4f}")
    print(f"Portfolio Sharpe Ratio: {sharpe:.4f}")
    print(f"Continuous Growth Rate g*: {g_star:.4f}")
    print(f"Identity check: r + 0.5 * SR^2 = {r + 0.5 * (sharpe**2):.4f}")
    print("\nNumeraire Martingale Property E[(S_i(t)/W*(t))] (Theoretical = 1.0000):")
    for i, mean_val in enumerate(deflated_means):
        print(f"Asset {i + 1} Deflated Expectation: {mean_val:.4f}")


main()
