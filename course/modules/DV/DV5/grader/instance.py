"""Instance generator for DV5: Variance Risk Premium & Volatility Trading.

Generates deterministic market instances across seeds 0-49:
- Synthetic option chains for model-free implied volatility / VIX replication.
- Realized underlying price paths for variance swap settlement.
- Daily market series (spot, VIX, realized variance) for short-volatility strategy backtesting.
- Margin requirements, leverage parameters, transaction costs, and stress scenarios (2008, 2018, 2020).
All simulated data is labeled SIMULATED.
All dictionary values are numeric primitives or lists of numeric tuples for deterministic reproducibility.
"""

from __future__ import annotations

import math
import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Return a deterministic market instance for the given integer seed."""
    rng = random.Random(seed)

    spot = round(4000.0 + rng.random() * 500.0, 2)
    rate = round(0.015 + rng.random() * 0.025, 4)
    maturity = 30.0 / 365.0  # 30-day constant maturity
    forward = round(spot * math.exp(rate * maturity), 2)

    # 1. Option Chain for VIX Replication (SIMULATED)
    # Strikes spanning 85% to 115% of forward in steps of 25
    base_iv = 0.18 + rng.random() * 0.06  # 18% to 24%
    skew_param = 0.10 + rng.random() * 0.06
    smile_param = 0.20 + rng.random() * 0.10

    strike_step = 25.0
    k_min = math.floor((spot * 0.85) / strike_step) * strike_step
    k_max = math.ceil((spot * 1.15) / strike_step) * strike_step

    # Store options as tuples: (strike, is_call, bid, ask) where is_call is 1.0 (call) or 0.0 (put)
    options_chain: list[tuple[float, float, float, float]] = []
    k_current = k_min

    def bs_put(s: float, k: float, t: float, r: float, sig: float) -> float:
        if sig <= 0.0 or t <= 0.0:
            return max(0.0, k * math.exp(-r * t) - s)
        d1 = (math.log(s / k) + (r + 0.5 * sig * sig) * t) / (sig * math.sqrt(t))
        d2 = d1 - sig * math.sqrt(t)
        n_neg_d1 = 0.5 * (1.0 + math.erf(-d1 / math.sqrt(2.0)))
        n_neg_d2 = 0.5 * (1.0 + math.erf(-d2 / math.sqrt(2.0)))
        return k * math.exp(-r * t) * n_neg_d2 - s * n_neg_d1

    def bs_call(s: float, k: float, t: float, r: float, sig: float) -> float:
        if sig <= 0.0 or t <= 0.0:
            return max(0.0, s - k * math.exp(-r * t))
        d1 = (math.log(s / k) + (r + 0.5 * sig * sig) * t) / (sig * math.sqrt(t))
        d2 = d1 - sig * math.sqrt(t)
        n_d1 = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))
        n_d2 = 0.5 * (1.0 + math.erf(d2 / math.sqrt(2.0)))
        return s * n_d1 - k * math.exp(-r * t) * n_d2

    while k_current <= k_max:
        m = math.log(k_current / forward)
        iv_k = max(0.08, base_iv - skew_param * m + smile_param * (m**2))

        p_theoretical = bs_put(spot, k_current, maturity, rate, iv_k)
        c_theoretical = bs_call(spot, k_current, maturity, rate, iv_k)

        half_spread = max(0.05, 0.05 + 0.10 * abs(m))

        # Puts (is_call = 0.0)
        p_mid = p_theoretical
        p_bid = round(max(0.0, p_mid - half_spread), 2)
        p_ask = round(p_mid + half_spread, 2)
        if p_bid > 0.0 or k_current <= forward:
            options_chain.append((float(k_current), 0.0, float(p_bid), float(p_ask)))

        # Calls (is_call = 1.0)
        c_mid = c_theoretical
        c_bid = round(max(0.0, c_mid - half_spread), 2)
        c_ask = round(c_mid + half_spread, 2)
        if c_bid > 0.0 or k_current >= forward:
            options_chain.append((float(k_current), 1.0, float(c_bid), float(c_ask)))

        k_current += strike_step

    # 2. Realized underlying price path (22 trading days, 1 month)
    realized_vol_target = round(base_iv * (0.80 + rng.random() * 0.35), 4)
    daily_dt = 1.0 / 252.0
    daily_vol = realized_vol_target * math.sqrt(daily_dt)

    realized_prices: list[float] = [spot]
    curr_p = spot
    for _ in range(21):
        z = rng.gauss(0.0, 1.0)
        ret = (rate - 0.5 * daily_vol * daily_vol) * daily_dt + daily_vol * z
        curr_p = round(curr_p * math.exp(ret), 2)
        realized_prices.append(curr_p)

    var_swap_strike = round(base_iv**2, 5)
    var_swap_vega_notional = round(50000.0 + rng.random() * 50000.0, 2)

    # 3. Market time series for backtesting (60 trading days)
    # Stored as tuples: (day, spot, vix, rv_realized)
    market_data: list[tuple[float, float, float, float]] = []
    mkt_spot = spot
    mkt_vix = round(base_iv * 100.0, 2)

    for day in range(60):
        z_spot = rng.gauss(0.0, 1.0)
        z_ortho = rng.gauss(0.0, 1.0)
        rho_sv = -0.75
        z_vix = rho_sv * z_spot + math.sqrt(1.0 - rho_sv**2) * z_ortho

        vol_current = (mkt_vix / 100.0) * math.sqrt(daily_dt)
        spot_ret = 0.0003 + vol_current * z_spot
        mkt_spot = round(mkt_spot * math.exp(spot_ret), 2)

        vix_speed = 0.12
        vix_mean = base_iv * 100.0
        vix_diff = vix_speed * (vix_mean - mkt_vix) + 1.8 * z_vix
        mkt_vix = round(max(9.0, min(85.0, mkt_vix + vix_diff)), 2)
        rv_day = round((spot_ret**2) * 252.0, 5)

        market_data.append((float(day), float(mkt_spot), float(mkt_vix), float(rv_day)))

    initial_capital = round(1000000.0 + rng.random() * 500000.0, 2)
    target_leverage = round(1.2 + rng.random() * 0.8, 2)
    margin_requirement = round(0.18 + rng.random() * 0.05, 4)
    transaction_cost_bps = round(6.0 + rng.random() * 6.0, 2)

    # Stress scenarios: (spot_shock, vix_shock)
    stress_shocks: list[tuple[float, float]] = [(-0.20, 35.0), (-0.041, 20.0), (-0.12, 45.0)]
    stress_names: list[str] = ["2008_lehman", "2018_volmageddon", "2020_covid"]

    return {
        "seed": seed,
        "spot": spot,
        "forward": forward,
        "rate": rate,
        "maturity": maturity,
        "options_chain": options_chain,
        "realized_prices": realized_prices,
        "var_swap_strike": var_swap_strike,
        "var_swap_vega_notional": var_swap_vega_notional,
        "market_data": market_data,
        "initial_capital": initial_capital,
        "target_leverage": target_leverage,
        "margin_requirement": margin_requirement,
        "transaction_cost_bps": transaction_cost_bps,
        "stress_shocks": stress_shocks,
        "stress_names": stress_names,
    }
