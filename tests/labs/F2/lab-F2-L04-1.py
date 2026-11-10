"""Lab F2-L04-1: Betting Against Beta (BAB) and Idiosyncratic Volatility (IVOL).

Constructs the Frazzini-Pedersen (2014) Betting Against Beta factor using empirical
beta shrinking, leverage scaling, and ex-ante beta neutrality, and tests the Ang et al.
(2006) idiosyncratic volatility puzzle across quintile portfolios.
"""

from __future__ import annotations

import numpy as np


def simulate_bab_and_ivol(seed: int = 42) -> dict[str, float | int]:
    """Construct BAB portfolio and evaluate IVOL quintile returns."""
    rng = np.random.default_rng(seed)
    n_stocks = 250
    n_months = 180

    # True market factor: 6% mean, 15% vol
    mkt = rng.normal(0.06 / 12, 0.15 / np.sqrt(12), size=n_months)

    # True dispersion in market betas: [0.4, 1.8]
    true_betas = rng.uniform(0.4, 1.8, size=n_stocks)

    # High-beta stocks have lottery/distress characteristics and higher IVOL
    ivol_true = 0.10 + 0.15 * (true_betas - 0.4) + rng.uniform(0.05, 0.20, size=n_stocks)

    # Security returns: Black (1972) flat security market line
    # High-beta stocks earn flat or lower risk-adjusted returns (alpha penalty on high beta / high IVOL)
    alpha_penalty = -0.04 * (true_betas - 1.0) / 12.0  # low beta earns positive alpha, high beta negative

    stock_rets = np.zeros((n_months, n_stocks))
    for t in range(n_months):
        idio = rng.normal(0, ivol_true / np.sqrt(12), size=n_stocks)
        stock_rets[t, :] = alpha_penalty + true_betas * mkt[t] + idio

    # Vasicek / Bayesian shrinkage of historical betas: beta_shrunk = 0.6 * beta_sample + 0.4 * 1.0
    sample_betas = np.zeros(n_stocks)
    for i in range(n_stocks):
        cov = np.cov(stock_rets[:, i], mkt)[0, 1]
        sample_betas[i] = cov / np.var(mkt)

    shrunk_betas = 0.6 * sample_betas + 0.4 * 1.0

    # Sort into Low Beta (bottom 50%) and High Beta (top 50%)
    median_beta = float(np.median(shrunk_betas))
    low_mask = shrunk_betas <= median_beta
    high_mask = shrunk_betas > median_beta

    # Value/equal weights within legs normalized by beta distance
    # Frazzini & Pedersen rank weights:
    beta_low = float(np.mean(shrunk_betas[low_mask]))
    beta_high = float(np.mean(shrunk_betas[high_mask]))

    r_low = np.mean(stock_rets[:, low_mask], axis=1)
    r_high = np.mean(stock_rets[:, high_mask], axis=1)

    # BAB factor: 1/beta_low * r_low - 1/beta_high * r_high
    r_bab = (1.0 / beta_low) * r_low - (1.0 / beta_high) * r_high

    # Verify BAB beta against market
    bab_beta = float(np.cov(r_bab, mkt)[0, 1] / np.var(mkt))

    mean_bab_ann = float(np.mean(r_bab) * 12 * 100)
    vol_bab_ann = float(np.std(r_bab, ddof=1) * np.sqrt(12) * 100)
    sharpe_bab = float(mean_bab_ann / vol_bab_ann)

    # Idiosyncratic volatility sort (quintiles Q1 low IVOL to Q5 high IVOL)
    ivol_sample = np.std(stock_rets - np.outer(mkt, sample_betas), axis=0, ddof=1) * np.sqrt(12)
    q_bounds = np.percentile(ivol_sample, [20, 40, 60, 80])
    q1_ret = np.mean(stock_rets[:, ivol_sample <= q_bounds[0]], axis=1)
    q5_ret = np.mean(stock_rets[:, ivol_sample >= q_bounds[3]], axis=1)

    q1_mean_ann = float(np.mean(q1_ret) * 12 * 100)
    q5_mean_ann = float(np.mean(q5_ret) * 12 * 100)
    ivol_spread = q5_mean_ann - q1_mean_ann  # Ang et al. puzzle: Q5 - Q1 is negative!

    return {
        "n_stocks": n_stocks,
        "beta_low": round(beta_low, 2),
        "beta_high": round(beta_high, 2),
        "bab_beta_to_mkt": round(bab_beta, 3),
        "mean_bab_ann": round(mean_bab_ann, 2),
        "vol_bab_ann": round(vol_bab_ann, 2),
        "sharpe_bab": round(sharpe_bab, 2),
        "q1_low_ivol_ann": round(q1_mean_ann, 2),
        "q5_high_ivol_ann": round(q5_mean_ann, 2),
        "ivol_spread_ann": round(ivol_spread, 2),
    }


def main() -> None:
    print("Lab F2-L04-1 | Betting Against Beta (BAB) & IVOL Puzzle (Ang et al. 2006)")
    print("------------------------------------------------------------------------")
    res = simulate_bab_and_ivol(seed=42)
    print(f"Sample: {res['n_stocks']} equities; Shrunk Beta Low: {res['beta_low']:.2f}, High: {res['beta_high']:.2f}")
    print(f"BAB Realized Market Beta:    {res['bab_beta_to_mkt']:+.3f} (ex-ante beta neutral)")
    print(
        f"BAB Annualized Premium:      {res['mean_bab_ann']:+.2f}% "
        f"(vol {res['vol_bab_ann']:.2f}%, SR = {res['sharpe_bab']:.2f})"
    )
    print(f"Q1 (Low IVOL) Ann Return:    {res['q1_low_ivol_ann']:+.2f}%")
    print(f"Q5 (High IVOL) Ann Return:   {res['q5_high_ivol_ann']:+.2f}%")
    print(f"IVOL Spread (Q5 - Q1):       {res['ivol_spread_ann']:+.2f}% (IVOL Puzzle anomaly)")


main()
