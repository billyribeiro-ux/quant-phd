"""Lab AP7-L02-1: Hong & Stein (1999) Underreaction and Overreaction Dynamics.

SIMULATED: Simulates boundedly rational news-watchers (gradual information diffusion)
and momentum traders (trend chasing), reproducing short-term momentum and long-term
reversals in asset price changes (Hong & Stein 1999).
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    seed = 42
    rng = np.random.default_rng(seed)
    n_periods = 1200

    # Model parameters:
    # Information diffusion speed: news epsilon_t takes z periods to diffuse fully
    z_diffusion = 4  # news spreads across z equal cohorts of news watchers
    j_momentum = 3  # momentum traders look back j periods of past price changes
    phi_momentum = 0.65  # aggressiveness of momentum trend chasing

    # Fundamental dividend innovations: epsilon_t ~ N(0, sigma^2)
    innovations = rng.normal(0.0, 1.0, size=n_periods)

    # True fundamental value: random walk D_t = D_{t-1} + epsilon_t
    fundamentals = np.cumsum(innovations)

    # Price dynamics:
    # News-watchers' price adjustment without momentum traders:
    # P_t^NW = D_{t-z} + (1/z) * epsilon_{t-z+1} + ... + (z/z) * epsilon_t
    # Gradual diffusion causes underreaction to current news
    price_changes = np.zeros(n_periods)
    prices = np.zeros(n_periods)

    for t in range(z_diffusion, n_periods):
        # Gradual diffusion fundamental component
        diffusion_term = np.mean(innovations[t - z_diffusion + 1 : t + 1])

        # Momentum trader demand depends on recent price changes: sum_{k=1}^j Delta P_{t-k}
        recent_momentum = np.sum(price_changes[t - j_momentum : t]) if t >= j_momentum else 0.0
        momentum_term = phi_momentum * (recent_momentum / j_momentum)

        # Price change at t combines gradual news absorption + momentum feedback
        price_changes[t] = diffusion_term + momentum_term - 0.20 * (prices[t - 1] - fundamentals[t - 1])
        prices[t] = prices[t - 1] + price_changes[t]

    # Analyze return autocorrelations across lags 1 to 12
    valid_changes = price_changes[z_diffusion + 10 :]
    lags = [1, 2, 3, 6, 9, 12]
    autocorrs = {}

    for lag in lags:
        c_val = np.corrcoef(valid_changes[lag:], valid_changes[:-lag])[0, 1]
        autocorrs[lag] = float(c_val)

    # Peak momentum lag and peak reversal lag
    max_autocorr_lag = max(autocorrs, key=lambda k: autocorrs[k])
    min_autocorr_lag = min(autocorrs, key=lambda k: autocorrs[k])

    print("Hong-Stein Return Autocorrelation Structure:")
    for lag in lags:
        print(f"  Lag {lag:2d} Autocorrelation: {autocorrs[lag]:+.4f}")
    print(f"Peak positive autocorrelation (momentum): lag {max_autocorr_lag} ({autocorrs[max_autocorr_lag]:+.4f})")
    print(f"Trough negative autocorrelation (reversal): lag {min_autocorr_lag} ({autocorrs[min_autocorr_lag]:+.4f})")
    print(f"Short-run momentum (lag 1 > 0):            {bool(autocorrs[1] > 0)}")
    print(f"Long-run reversal (lag 12 < 0):            {bool(autocorrs[12] < 0)}")


main()
