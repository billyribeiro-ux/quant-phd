"""Deterministic test instance generator for FI6 Swaption-Cube Engine.

Generates multi-curve term structures, market swaption volatility cube grid slices,
and off-grid target swaptions for calibration, arbitrage testing, and pricing.
All dictionary values are numeric primitives or pure numeric arrays to ensure deterministic hashing.
"""

from __future__ import annotations

import math
import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a reproducible, seed-dependent test instance with pure numeric arrays."""
    rng = random.Random(seed)

    # Tenor grid for zero curves (0.5Y to 30Y)
    tenors = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0]

    # Baseline zero rates with seed variation
    base_ois = round(0.0350 + 0.0100 * rng.random(), 4)  # 3.5% to 4.5%
    curve_slope = round(0.0050 + 0.0040 * rng.random(), 4)  # upward slope
    ois_zero_rates = [
        round(base_ois + curve_slope * (1.0 - math.exp(-t / 5.0)) + 0.0005 * math.sin(t), 6) for t in tenors
    ]

    # Projection curve carries a 20-40 bps basis spread
    basis_spread = round(0.0020 + 0.0020 * rng.random(), 4)
    proj_zero_rates = [
        round(r + basis_spread + 0.0002 * math.cos(t), 6) for r, t in zip(ois_zero_rates, tenors, strict=False)
    ]

    # Swaption cube grid
    grid_expiries = [1.0, 2.0, 5.0, 10.0]
    grid_tenors = [2.0, 5.0, 10.0]

    grid_fwd_rates: list[float] = []
    grid_annuities: list[float] = []
    grid_strikes: list[list[float]] = []
    grid_vols: list[list[float]] = []

    for texp in grid_expiries:
        for tenor in grid_tenors:
            fwd = round(
                max(base_ois + basis_spread + 0.0040 * (texp + tenor) / 15.0 + 0.0010 * rng.gauss(0.0, 0.5), 0.0150), 6
            )
            df_mid = math.exp(-base_ois * (texp + tenor / 2.0))
            annuity = round(tenor * df_mid * (1.0 + 0.02 * math.sin(texp)), 5)

            true_alpha = (0.030 + 0.010 * math.exp(-texp / 5.0)) * (fwd**0.5)
            true_rho = -0.35 + 0.15 * (tenor / 10.0)
            true_nu = 0.35 + 0.15 * math.exp(-tenor / 5.0)

            strike_offsets = [-0.0100, -0.0050, 0.0, 0.0050, 0.0100]
            strikes = [round(max(fwd + off, 0.0050), 5) for off in strike_offsets]

            vols: list[float] = []
            for k in strikes:
                log_fk = math.log(fwd / k)
                fk_mid = math.sqrt(fwd * k)
                denom = (fk_mid**0.5) * (1.0 + (1.0 / 96.0) * (log_fk**2))
                z = (true_nu / true_alpha) * (fk_mid**0.5) * log_fk
                if abs(z) < 1e-5:
                    zx = 1.0 - 0.5 * true_rho * z
                else:
                    rad = max(1.0 - 2.0 * true_rho * z + z**2, 0.0)
                    zx = z / math.log((math.sqrt(rad) + z - true_rho) / (1.0 - true_rho))
                t_term = (
                    1.0
                    + (
                        (1.0 / 96.0) * (true_alpha**2 / fk_mid)
                        + (true_rho * 0.5 * true_nu * true_alpha) / (4.0 * (fk_mid**0.5))
                        + ((2.0 - 3.0 * true_rho**2) / 24.0) * (true_nu**2)
                    )
                    * texp
                )
                v = (true_alpha / denom) * zx * t_term
                v += 0.0005 * rng.gauss(0.0, 1.0)
                vols.append(round(max(v, 0.05), 5))

            grid_fwd_rates.append(fwd)
            grid_annuities.append(annuity)
            grid_strikes.append(strikes)
            grid_vols.append(vols)

    # Off-grid test targets for pricing and Greeks evaluation
    off_grid_texp = [1.5, 3.0, 7.0, 0.5]
    off_grid_tenor = [3.0, 7.0, 4.0, 5.0]
    off_grid_strike = [
        round(base_ois + 0.0020, 4),
        round(base_ois + 0.0050, 4),
        round(base_ois + 0.0070, 4),
        round(base_ois - 0.0020, 4),
    ]
    off_grid_is_payer = [1, 0, 1, 0]  # 1 for True, 0 for False

    return {
        "base_ois": base_ois,
        "basis_spread": basis_spread,
        "grid_annuities": grid_annuities,
        "grid_expiries": grid_expiries,
        "grid_fwd_rates": grid_fwd_rates,
        "grid_strikes": grid_strikes,
        "grid_tenors": grid_tenors,
        "grid_vols": grid_vols,
        "off_grid_is_payer": off_grid_is_payer,
        "off_grid_strike": off_grid_strike,
        "off_grid_tenor": off_grid_tenor,
        "off_grid_texp": off_grid_texp,
        "ois_zero_rates": ois_zero_rates,
        "proj_zero_rates": proj_zero_rates,
        "seed": seed,
        "tenors": tenors,
    }


def unpack_market_grid(inst: dict[str, Any]) -> dict[str, Any]:
    """Helper to reconstruct the keyed market_grid dictionary from numeric arrays."""
    grid_expiries: list[float] = inst["grid_expiries"]
    grid_tenors: list[float] = inst["grid_tenors"]
    fwd_rates: list[float] = inst["grid_fwd_rates"]
    annuities: list[float] = inst["grid_annuities"]
    strikes: list[list[float]] = inst["grid_strikes"]
    vols: list[list[float]] = inst["grid_vols"]

    market_grid: dict[str, Any] = {}
    idx = 0
    for texp in grid_expiries:
        for tenor in grid_tenors:
            key = f"{texp:.1f}x{tenor:.1f}"
            market_grid[key] = {
                "texp": texp,
                "tenor": tenor,
                "fwd": fwd_rates[idx],
                "annuity": annuities[idx],
                "strikes": strikes[idx],
                "vols": vols[idx],
            }
            idx += 1
    return market_grid
