"""Instance generator for DV2: The Volatility Surface (Arbitrage-Free Surface Builder).

Generates deterministic market option chains across multiple expiries and strikes,
with benchmark SVI parameters and evaluation grids.
All instances are labeled SIMULATED.
All dictionary values are numeric primitives or pure numeric arrays to ensure deterministic hashing.
"""

from __future__ import annotations

import math
import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Return a deterministic market instance for the given integer seed."""
    rng = random.Random(seed)

    spot = round(90.0 + rng.random() * 30.0, 2)
    rate = round(0.02 + rng.random() * 0.03, 4)
    dividend = round(0.005 + rng.random() * 0.015, 4)

    # 4 expiries from 3 months to 1 year
    expiries = [0.25, 0.50, 0.75, 1.00]
    forwards = [round(spot * math.exp((rate - dividend) * t), 4) for t in expiries]

    # Deterministic base SVI parameters across expiries, guaranteed free of butterfly and calendar arbitrage
    # SVI total variance w(k) = a + b * (rho * (k - m) + sqrt((k - m)^2 + sigma^2))
    base_rho = round(-0.35 + rng.random() * 0.10, 4)  # negative equity skew
    base_m_slope = round(0.015 + rng.random() * 0.010, 4)

    svi_a: list[float] = []
    svi_b: list[float] = []
    svi_rho: list[float] = []
    svi_m: list[float] = []
    svi_sigma: list[float] = []

    for i, t in enumerate(expiries):
        a_val = round(0.035 * t + 0.002 * (i + 1), 6)
        b_val = round(0.110 * math.sqrt(t) + 0.005 * i, 6)
        m_val = round(base_m_slope * t, 6)
        sigma_val = round(0.090 * math.sqrt(t) + 0.005 * (i + 1), 6)

        svi_a.append(a_val)
        svi_b.append(b_val)
        svi_rho.append(base_rho)
        svi_m.append(m_val)
        svi_sigma.append(sigma_val)

    # Generate synthetic market option quotes (SIMULATED) with small pseudo-random noise
    k_quotes = [-0.50, -0.35, -0.20, -0.10, -0.05, 0.0, 0.05, 0.10, 0.20, 0.35, 0.50]
    market_strikes: list[list[float]] = []
    market_log_moneyness: list[list[float]] = []
    market_implied_vol: list[list[float]] = []
    market_total_variance: list[list[float]] = []

    for i, t in enumerate(expiries):
        fwd = forwards[i]
        a_val, b_val, rho_val, m_val, sigma_val = svi_a[i], svi_b[i], svi_rho[i], svi_m[i], svi_sigma[i]

        row_strikes: list[float] = []
        row_k: list[float] = []
        row_vol: list[float] = []
        row_w: list[float] = []

        for k in k_quotes:
            strike = round(fwd * math.exp(k), 2)
            actual_k = math.log(strike / fwd)
            diff = actual_k - m_val
            root = math.sqrt(diff**2 + sigma_val**2)
            w_true = a_val + b_val * (rho_val * diff + root)
            bs_vol = math.sqrt(max(1e-4, w_true / t))
            vol_noise = (rng.random() - 0.5) * 0.002
            noisy_vol = round(max(0.05, bs_vol + vol_noise), 5)
            w_noisy = round(noisy_vol**2 * t, 6)

            row_strikes.append(strike)
            row_k.append(round(actual_k, 5))
            row_vol.append(noisy_vol)
            row_w.append(w_noisy)

        market_strikes.append(row_strikes)
        market_log_moneyness.append(row_k)
        market_implied_vol.append(row_vol)
        market_total_variance.append(row_w)

    # Dense log-moneyness grid for arbitrage verification and local volatility extraction
    dense_k = [round(-1.2 + 0.1 * j, 2) for j in range(25)]

    return {
        "spot": spot,
        "rate": rate,
        "dividend": dividend,
        "expiries": expiries,
        "forwards": forwards,
        "svi_a": svi_a,
        "svi_b": svi_b,
        "svi_rho": svi_rho,
        "svi_m": svi_m,
        "svi_sigma": svi_sigma,
        "market_strikes": market_strikes,
        "market_log_moneyness": market_log_moneyness,
        "market_implied_vol": market_implied_vol,
        "market_total_variance": market_total_variance,
        "k_eval_grid": dense_k,
        "seed": seed,
    }
