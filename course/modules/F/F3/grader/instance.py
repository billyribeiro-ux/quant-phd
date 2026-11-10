"""Instance generator for Module F3 Project: Multi-Asset Factor Book.

Generates reproducible multi-asset monthly return panels and factor signals
across three asset classes (Rates, FX, Commodities) over 30 years (T=360 months).
"""

from __future__ import annotations

import functools

import numpy as np


@functools.lru_cache(maxsize=128)
def make_instance(seed: int) -> dict[str, object]:
    """Generate deterministic multi-asset return panels and factor signals.

    Parameters
    ----------
    seed : int
        RNG seed for reproducibility.

    Returns
    -------
    dict[str, object]
        Contains returns, carry signals, and value signals across Rates, FX,
        and Commodities, alongside asset metadata.
    """
    rng = np.random.default_rng(seed)
    n_months = 360  # 30 years
    n_assets_per_class = 4
    dt = 1.0 / 12.0

    growth = rng.normal(0.04 * dt, 0.12 * np.sqrt(dt), size=n_months)
    inflation = rng.normal(0.02 * dt, 0.08 * np.sqrt(dt), size=n_months)

    # -------------------------------------------------------------
    # 1. Rates (Government Bond Futures: US 10Y, GER Bund, UK Gilt, JPN JGB)
    # -------------------------------------------------------------
    rates_returns = np.zeros((n_months, n_assets_per_class))
    rates_carry = np.zeros((n_months, n_assets_per_class))
    rates_value = np.zeros((n_months, n_assets_per_class))

    base_term_spreads = np.array([0.028, 0.018, 0.022, 0.008])
    for i in range(n_assets_per_class):
        rates_carry[:, i] = base_term_spreads[i] + rng.normal(0, 0.004, size=n_months)
        # Value signal: mean-reverting valuation deviation
        rates_value[:, i] = rng.normal(0, 0.05, size=n_months)

    for t in range(n_months):
        for i in range(n_assets_per_class):
            idio = rng.normal(0.0, 0.04 * np.sqrt(dt))
            carry_drift = 0.5 * rates_carry[t, i] * dt
            val_drift = 0.25 * rates_value[t, i] * dt
            mom_drift = 0.0
            if t >= 12:
                past_12m = np.sum(rates_returns[t - 12 : t, i])
                mom_drift = 0.12 * np.sign(past_12m) * dt
            rates_returns[t, i] = (
                0.012 * dt + carry_drift + val_drift + mom_drift - 0.4 * growth[t] - 0.5 * inflation[t] + idio
            )

    # -------------------------------------------------------------
    # 2. FX (Currency Pairs vs USD: AUD, EUR, GBP, JPY)
    # -------------------------------------------------------------
    fx_returns = np.zeros((n_months, n_assets_per_class))
    fx_carry = np.zeros((n_months, n_assets_per_class))
    fx_value = np.zeros((n_months, n_assets_per_class))

    base_fx_diffs = np.array([0.035, 0.010, 0.018, -0.012])
    for i in range(n_assets_per_class):
        fx_carry[:, i] = base_fx_diffs[i] + rng.normal(0, 0.003, size=n_months)
        fx_value[:, i] = rng.normal(0, 0.06, size=n_months)

    for t in range(n_months):
        jump_event = rng.uniform(0, 1) < 0.025
        jump_shock = rng.normal(-0.06, 0.02) if jump_event else 0.0
        for i in range(n_assets_per_class):
            idio = rng.normal(0.0, 0.08 * np.sqrt(dt))
            carry_drift = 0.6 * fx_carry[t, i] * dt
            val_drift = 0.28 * fx_value[t, i] * dt
            mom_drift = 0.0
            if t >= 12:
                past_12m = np.sum(fx_returns[t - 12 : t, i])
                mom_drift = 0.14 * np.sign(past_12m) * dt
            jump_extra = jump_shock if base_fx_diffs[i] > 0.015 else 0.0
            fx_returns[t, i] = carry_drift + val_drift + mom_drift + 0.3 * growth[t] + jump_extra + idio

    # -------------------------------------------------------------
    # 3. Commodities (Crude Oil, Gold, Copper, Agriculture)
    # -------------------------------------------------------------
    comm_returns = np.zeros((n_months, n_assets_per_class))
    comm_carry = np.zeros((n_months, n_assets_per_class))
    comm_value = np.zeros((n_months, n_assets_per_class))

    base_roll_yields = np.array([0.05, -0.01, 0.04, -0.02])
    for i in range(n_assets_per_class):
        comm_carry[:, i] = base_roll_yields[i] + rng.normal(0, 0.015, size=n_months)
        comm_value[:, i] = rng.normal(0, 0.08, size=n_months)

    for t in range(n_months):
        for i in range(n_assets_per_class):
            idio = rng.normal(0.0, 0.15 * np.sqrt(dt))
            carry_drift = 0.6 * comm_carry[t, i] * dt
            val_drift = 0.30 * comm_value[t, i] * dt
            mom_drift = 0.0
            if t >= 12:
                past_12m = np.sum(comm_returns[t - 12 : t, i])
                mom_drift = 0.16 * np.sign(past_12m) * dt
            comm_returns[t, i] = (
                0.015 * dt + carry_drift + val_drift + mom_drift + 0.7 * growth[t] + 0.8 * inflation[t] + idio
            )

    return {
        "seed": int(seed),
        "n_months": int(n_months),
        "asset_classes": ["rates", "fx", "commodities"],
        "rates": {
            "names": ["US_10Y", "GER_BUND", "UK_GILT", "JPN_JGB"],
            "returns": rates_returns,
            "carry": rates_carry,
            "value": rates_value,
        },
        "fx": {
            "names": ["AUD_USD", "EUR_USD", "GBP_USD", "USD_JPY"],
            "returns": fx_returns,
            "carry": fx_carry,
            "value": fx_value,
        },
        "commodities": {
            "names": ["CRUDE_OIL", "GOLD", "COPPER", "AGRICULTURE"],
            "returns": comm_returns,
            "carry": comm_carry,
            "value": comm_value,
        },
    }
