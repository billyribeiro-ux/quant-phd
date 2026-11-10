"""Deterministic instance generator for the PM4 MBS pricer project.

Generates realistic mortgage collateral, short-rate diffusion, prepayment incentive,
and market target specifications for a given integer seed.
"""

from __future__ import annotations

import numpy as np


def make_instance(seed: int) -> dict[str, float | int]:
    """Generate a deterministic, flat MBS pricing instance dictionary for a given seed."""
    rng = np.random.default_rng(seed)

    # 1. Collateral Pool Specification
    wac = 0.055 + (seed % 15) * 0.001  # 5.50% to 6.90%
    servicing_gfee = 0.0050  # 50 bps total servicing and guarantee fee
    pass_through_rate = wac - servicing_gfee
    wam = 360  # 30-year fixed
    notional = 100_000_000.0  # $100M baseline pool
    delay_days = 24  # Fannie Mae / Freddie Mac standard actual delay

    # 2. Short-Rate Term Structure (Vasicek 1-factor)
    r0 = 0.040 + (seed % 9) * 0.002  # 4.00% to 5.60%
    kappa = 0.12 + (seed % 7) * 0.01  # 0.12 to 0.18
    theta = 0.045 + (seed % 8) * 0.002  # 4.50% to 5.90%
    sigma = 0.012 + (seed % 5) * 0.001  # 1.20% to 1.60%

    # 3. Prepayment & Burnout Specification
    base_cpr = 0.05 + (seed % 5) * 0.003  # 5.0% to 6.2%
    max_cpr = 0.35 + (seed % 6) * 0.015  # 35.0% to 42.5%
    beta = 50.0 + (seed % 5) * 4.0  # 50.0 to 66.0
    mu = 0.008 + (seed % 5) * 0.001  # 80 bps to 120 bps incentive threshold
    margin = 0.012 + (seed % 4) * 0.001  # 120 bps to 150 bps mortgage margin
    gamma_burnout = 0.04 + (seed % 5) * 0.004  # 0.04 to 0.056 burnout rate

    # 4. Target Market Price for OAS Calibration
    price_factor = 0.985 + float(rng.uniform(0.005, 0.040))
    target_market_price = float(round(notional * price_factor, 2))

    return {
        "seed": seed,
        "notional": notional,
        "wac": float(round(wac, 5)),
        "pass_through_rate": float(round(pass_through_rate, 5)),
        "wam": wam,
        "delay_days": delay_days,
        "r0": float(round(r0, 5)),
        "kappa": float(round(kappa, 4)),
        "theta": float(round(theta, 5)),
        "sigma": float(round(sigma, 5)),
        "base_cpr": float(round(base_cpr, 4)),
        "max_cpr": float(round(max_cpr, 4)),
        "beta": float(round(beta, 2)),
        "mu": float(round(mu, 4)),
        "margin": float(round(margin, 4)),
        "gamma_burnout": float(round(gamma_burnout, 4)),
        "n_paths": 500,
        "target_market_price": target_market_price,
        "dy": 0.0025,
        "sim_seed": 42 + seed * 1007,
    }
