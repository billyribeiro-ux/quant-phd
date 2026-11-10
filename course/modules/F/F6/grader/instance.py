"""Instance generator for F6: Machine Learning in Asset Pricing.

Generates realistic, deterministic cross-sectional panels of firm characteristics,
time-series returns with low signal-to-noise ratios, non-linear interactions,
and transaction cost parameters.
"""

from __future__ import annotations

import numpy as np


def make_instance(seed: int) -> dict[str, object]:
    """Generate a reproducible, seed-dependent asset pricing ML panel instance.

    Parameters
    ----------
    seed : int
        Pseudorandom generator seed.

    Returns
    -------
    dict[str, object]
        Instance dictionary containing:
        - 'N': number of assets
        - 'T_train': number of training time periods
        - 'T_test': number of testing time periods
        - 'P': number of firm characteristics
        - 'X_train': training characteristics array of shape (N, T_train, P)
        - 'y_train': training forward excess returns of shape (N, T_train)
        - 'X_test': test characteristics array of shape (N, T_test, P)
        - 'y_test': test forward excess returns of shape (N, T_test)
        - 'cost_bps': round-trip transaction cost in basis points
        - 'gammas': complexity parameter ratios for double descent test
    """
    rng = np.random.default_rng(seed)

    n_assets = 24
    t_train = 40
    t_test = 24
    t_total = t_train + t_test
    n_features = 8

    # Generate persistent characteristics: AR(1) dynamics with cross-sectional normalization
    raw_x = np.zeros((n_assets, t_total, n_features), dtype=np.float64)
    phi = 0.92  # high persistence characteristic
    x_prev = rng.normal(0.0, 1.0, size=(n_assets, n_features))

    for t in range(t_total):
        innov = rng.normal(0.0, 0.3, size=(n_assets, n_features))
        x_prev = phi * x_prev + innov
        # Cross-sectional rank transform to [-0.5, 0.5] to prevent outliers
        for p in range(n_features):
            ranks = np.argsort(np.argsort(x_prev[:, p]))
            raw_x[:, t, p] = (ranks / (n_assets - 1)) - 0.5

    # True return-generating process:
    # 1. Linear effects on features 0, 1
    # 2. Non-linear interaction between feature 0 and feature 2
    # 3. Macro regime factor interacting with feature 3
    # 4. Latent market factor and idiosyncratic noise (low S/N ratio ~ 2%)
    beta_linear = np.array([0.025, -0.020, 0.015, -0.010, 0.005, 0.0, 0.0, 0.0], dtype=np.float64)
    macro_factor = rng.normal(0.0, 0.04, size=t_total)
    market_return = rng.normal(0.006, 0.045, size=t_total)

    y_total = np.zeros((n_assets, t_total), dtype=np.float64)
    for t in range(t_total):
        x_t = raw_x[:, t, :]  # (N, P)
        signal_lin = x_t @ beta_linear
        signal_inter = 0.035 * (x_t[:, 0] * x_t[:, 2])
        signal_macro = 0.020 * (x_t[:, 3] * macro_factor[t])

        # Market exposure (beta around 1.0)
        stock_betas = 0.8 + 0.4 * (x_t[:, 1] + 0.5)
        mkt_comp = stock_betas * market_return[t]

        idio_noise = rng.normal(0.0, 0.065, size=n_assets)
        y_total[:, t] = signal_lin + signal_inter + signal_macro + mkt_comp + idio_noise

    x_train = raw_x[:, :t_train, :]
    y_train = y_total[:, :t_train]
    x_test = raw_x[:, t_train:, :]
    y_test = y_total[:, t_train:]

    cost_bps = float(10.0 + (seed % 10))  # 10 to 19 bps
    gammas = [0.25, 0.5, 0.9, 1.0, 1.5, 2.5, 4.0]

    return {
        "N": n_assets,
        "T_train": t_train,
        "T_test": t_test,
        "P": n_features,
        "X_train": x_train,
        "y_train": y_train,
        "X_test": x_test,
        "y_test": y_test,
        "cost_bps": cost_bps,
        "gammas": gammas,
    }
