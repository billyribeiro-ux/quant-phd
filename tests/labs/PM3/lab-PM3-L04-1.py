"""Lab PM3-L04-1: Private Credit Return Smoothing and AR(1) De-Smoothing Engine.

SIMULATED: Demonstrates appraisal smoothing distortions on illiquid private credit returns,
quantifying observed vs. true volatility, beta to leveraged loans, and Sharpe ratio inflation.
"""

from __future__ import annotations

import numpy as np


def simulate_smoothed_credit_returns(
    n_quarters: int = 60,
    phi: float = 0.55,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate true and appraisal-smoothed private credit returns against a public loan proxy.

    Parameters
    ----------
    n_quarters : int
        Number of quarterly periods to simulate (e.g. 60 quarters = 15 years).
    phi : float
        Appraisal smoothing coefficient (decay factor in [0, 1)).
    seed : int
        RNG seed for deterministic evaluation.

    Returns
    -------
    tuple[np.ndarray, np.ndarray, np.ndarray]
        (r_loan, r_true, r_obs)
    """
    rng = np.random.default_rng(seed)
    mu_m = 0.018  # 1.8% per quarter (~7.2% annualized)
    sigma_m = 0.035  # 3.5% per quarter (~7.0% annualized)

    # Public syndicated loan proxy returns
    r_loan = rng.normal(mu_m, sigma_m, size=n_quarters)

    # True unobserved private credit returns: beta = 1.05, alpha = 40 bps / qtr, idiosyncratic noise
    alpha = 0.004
    beta = 1.05
    noise = rng.normal(0.0, 0.012, size=n_quarters)
    r_true = alpha + beta * r_loan + noise

    # Observed reported private credit returns under AR(1) appraisal smoothing
    r_obs = np.zeros(n_quarters)
    r_obs[0] = r_true[0]
    for t in range(1, n_quarters):
        r_obs[t] = phi * r_obs[t - 1] + (1.0 - phi) * r_true[t]

    return r_loan, r_true, r_obs


def estimate_ar1_phi(returns: np.ndarray) -> float:
    """Estimate the first-order serial correlation coefficient phi."""
    r_t = returns[1:]
    r_lag = returns[:-1]
    cov = np.cov(r_t, r_lag)[0, 1]
    var_lag = np.var(r_lag, ddof=1)
    phi = float(cov / var_lag) if var_lag > 0 else 0.0
    return float(np.clip(phi, 0.0, 0.95))


def unsmooth_returns(r_obs: np.ndarray, phi: float) -> np.ndarray:
    """Invert the AR(1) smoothing process to recover true unobserved returns."""
    r_unsmooth = np.zeros_like(r_obs)
    r_unsmooth[0] = r_obs[0]
    denom = 1.0 - phi
    for t in range(1, len(r_obs)):
        r_unsmooth[t] = (r_obs[t] - phi * r_obs[t - 1]) / denom
    return r_unsmooth


def compute_series_stats(r: np.ndarray, r_market: np.ndarray, rf_q: float = 0.0075) -> dict[str, float]:
    """Calculate annualized mean, volatility, Sharpe ratio, and market beta."""
    mean_ann = float(np.mean(r) * 4.0)
    vol_ann = float(np.std(r, ddof=1) * 2.0)  # quarterly to annual: sqrt(4) = 2.0
    sharpe = float((mean_ann - rf_q * 4.0) / vol_ann) if vol_ann > 0 else 0.0

    cov_mat = np.cov(r, r_market)
    beta = float(cov_mat[0, 1] / cov_mat[1, 1]) if cov_mat[1, 1] > 0 else 0.0
    autocorr = float(np.corrcoef(r[1:], r[:-1])[0, 1])

    return {
        "mean_ann": mean_ann,
        "vol_ann": vol_ann,
        "sharpe": sharpe,
        "beta": beta,
        "autocorr": autocorr,
    }


def main() -> None:
    n_quarters = 60
    true_phi = 0.55
    r_loan, r_true, r_obs = simulate_smoothed_credit_returns(n_quarters, phi=true_phi, seed=42)

    hat_phi = estimate_ar1_phi(r_obs)
    r_recovered = unsmooth_returns(r_obs, hat_phi)

    rf_q = 0.0075  # 3.0% annualized risk-free rate

    stats_true = compute_series_stats(r_true, r_loan, rf_q)
    stats_obs = compute_series_stats(r_obs, r_loan, rf_q)
    stats_rec = compute_series_stats(r_recovered, r_loan, rf_q)
    stats_loan = compute_series_stats(r_loan, r_loan, rf_q)

    print("Private Credit Return Smoothing & De-Smoothing Engine Output:")
    print(f"True Simulation Smoothing Parameter (phi):  {true_phi:.4f}")
    print(f"Estimated Smoothing Parameter (hat_phi):   {hat_phi:.4f}\n")

    print("Metric                 | Public Loan Proxy | True Private Debt | Reported (Smoothed) | De-Smoothed")
    print("-" * 95)
    print(
        f"Annualized Mean (%)    | {stats_loan['mean_ann'] * 100:17.2f} | "
        f"{stats_true['mean_ann'] * 100:17.2f} | {stats_obs['mean_ann'] * 100:19.2f} | "
        f"{stats_rec['mean_ann'] * 100:11.2f}"
    )
    print(
        f"Annualized Vol (%)     | {stats_loan['vol_ann'] * 100:17.2f} | "
        f"{stats_true['vol_ann'] * 100:17.2f} | {stats_obs['vol_ann'] * 100:19.2f} | "
        f"{stats_rec['vol_ann'] * 100:11.2f}"
    )
    print(
        f"Annualized Sharpe      | {stats_loan['sharpe']:17.3f} | "
        f"{stats_true['sharpe']:17.3f} | {stats_obs['sharpe']:19.3f} | "
        f"{stats_rec['sharpe']:11.3f}"
    )
    print(
        f"Loan Market Beta       | {stats_loan['beta']:17.3f} | "
        f"{stats_true['beta']:17.3f} | {stats_obs['beta']:19.3f} | "
        f"{stats_rec['beta']:11.3f}"
    )
    print(
        f"First-Order Autocorr   | {stats_loan['autocorr']:17.3f} | "
        f"{stats_true['autocorr']:17.3f} | {stats_obs['autocorr']:19.3f} | "
        f"{stats_rec['autocorr']:11.3f}"
    )

    # Core theoretical assertions
    # 1. Observed reported volatility is strictly smaller than true volatility
    assert stats_obs["vol_ann"] < stats_true["vol_ann"] * 0.70

    # 2. Observed reported beta is strictly smaller than true beta
    assert stats_obs["beta"] < stats_true["beta"] * 0.70

    # 3. Observed Sharpe ratio is artificially inflated
    assert stats_obs["sharpe"] > stats_true["sharpe"] * 1.40

    # 4. De-smoothed volatility and beta expand towards true values
    assert stats_rec["vol_ann"] > stats_obs["vol_ann"] * 1.50
    assert stats_rec["beta"] > stats_obs["beta"] * 1.80
    assert np.isclose(stats_rec["vol_ann"], stats_true["vol_ann"], atol=0.015)
    assert np.isclose(stats_rec["beta"], stats_true["beta"], atol=0.25)

    print("\nDe-Smoothing Invariants: Verified true risk recovery, beta unbiasing, and Sharpe deflation.")


main()
