"""Lab 1 for PM2 L05: Selection Bias and Endogenous Censoring in VC Return Data.

SIMULATED: Econometric simulation of venture capital return censoring following Korteweg & Sorensen (2010).
Simulates 10,000 venture companies over a 3-year investment horizon (dt = 3.0 years).
Latent company log-valuation growth follows a Geometric Brownian Motion:
    Delta ln(V) ~ Normal((mu - 0.5 * sigma^2) * dt, sigma * sqrt(dt))
with true underlying parameters:
    mu_true = 0.12 (12.0% true expected annual return)
    sigma = 0.50 (50.0% annual idiosyncratic + systematic volatility).

Endogenous Selection Mechanism:
An intermediate round or exit valuation is observed with probability:
    P(Observed | Delta ln(V)) = 1 / (1 + exp(-gamma * (Delta ln(V) - theta)))
where gamma = 2.5 (selection sensitivity) and theta = -0.20 (censoring threshold).
Firms experiencing value destruction are systematically less likely to refinance or exit,
leaving their declining valuations unobserved (censored).

Standard library and NumPy only; fully deterministic with fixed seed.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    rng = np.random.default_rng(101)
    n_firms = 10_000
    dt = 3.0
    mu_true = 0.12
    sigma = 0.50

    # 1. Latent Value Evolution
    drift = (mu_true - 0.5 * sigma**2) * dt
    diffusion = sigma * np.sqrt(dt)
    z = rng.normal(0.0, 1.0, n_firms)
    log_growth = drift + diffusion * z
    simple_annualized_returns = np.exp(log_growth / dt) - 1.0

    # True population parameters
    pop_mean_return = float(np.mean(simple_annualized_returns))
    pop_median_return = float(np.median(simple_annualized_returns))

    # 2. Endogenous Selection (Korteweg & Sorensen 2010)
    gamma = 2.5
    theta = -0.20
    p_observed = 1.0 / (1.0 + np.exp(-gamma * (log_growth - theta)))
    u = rng.uniform(0.0, 1.0, n_firms)
    observed_mask = u < p_observed

    # Sample statistics among observed rounds
    observed_annualized_returns = simple_annualized_returns[observed_mask]
    obs_mean_return = float(np.mean(observed_annualized_returns))
    obs_median_return = float(np.median(observed_annualized_returns))

    # Selection bias gap
    bias_mean = obs_mean_return - pop_mean_return
    obs_median_return - pop_median_return

    # Censoring rates for winners vs losers
    losers_mask = simple_annualized_returns < 0.0
    censored_losers_pct = (1.0 - float(np.mean(observed_mask[losers_mask]))) * 100.0
    winners_mask = simple_annualized_returns > 0.30
    censored_winners_pct = (1.0 - float(np.mean(observed_mask[winners_mask]))) * 100.0

    print(f"Total Simulated Ventures: {n_firms:,}")
    print(f"Observed Refinancing / Exit Events: {int(np.sum(observed_mask)):,} ({np.mean(observed_mask) * 100:.1f}%)")
    print(f"True Population Mean Return: {pop_mean_return * 100:.2f}% (Median: {pop_median_return * 100:.2f}%)")
    print(f"Observed Sample Mean Return: {obs_mean_return * 100:.2f}% (Median: {obs_median_return * 100:.2f}%)")
    print(f"Selection Bias Gap in Mean Return: +{bias_mean * 100:.2f}% (+{bias_mean * 1e4:.0f} bps)")
    print(f"Censoring Rate for Value-Destructive Ventures: {censored_losers_pct:.1f}%")
    print(f"Censoring Rate for High-Growth Ventures (>30% ret): {censored_winners_pct:.1f}%")


main()
