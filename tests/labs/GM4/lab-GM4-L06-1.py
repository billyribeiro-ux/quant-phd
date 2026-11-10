"""Lab GM4-L06-1: Scenario P&L and Non-Linear Tail Stress Testing.

Evaluates a multi-asset macro portfolio across four canonical macroeconomic
stress scenarios, comparing linear Greek approximations with full non-linear revaluation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Scenario:
    name: str
    rates_slope_shock_bps: float
    fx_carry_shock_pct: float
    equity_spot_shock_pct: float
    vol_shock_pts: float


def bsm_call_pnl(s0: float, s1: float, k: float, v0: float, v1: float, t: float, r: float) -> tuple[float, float]:
    """Calculate (full_nonlinear_pnl, linear_delta_approx_pnl)."""

    # Helper for analytical price
    def price(s: float, vol: float) -> float:
        sqt = vol * math.sqrt(t)
        d1 = (math.log(s / k) + (r + 0.5 * vol * vol) * t) / sqt
        d2 = d1 - sqt
        c1 = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))
        c2 = 0.5 * (1.0 + math.erf(d2 / math.sqrt(2.0)))
        return s * c1 - k * math.exp(-r * t) * c2

    p0 = price(s0, v0)
    p1 = price(s1, v1)
    nonlinear_pnl = p1 - p0

    # Initial Delta
    sqt = v0 * math.sqrt(t)
    d1 = (math.log(s0 / k) + (r + 0.5 * v0 * v0) * t) / sqt
    delta = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))
    linear_pnl = delta * (s1 - s0)

    return nonlinear_pnl, linear_pnl


def main() -> None:
    # Portfolio composition:
    # 1. 2s10s Curve Steepener ($10M notional, DV01 neutrality, pays off when slope widens)
    # 2. FX Carry: Long AUD, Short JPY ($5M notional)
    # 3. Long Equity Volatility Straddle ($2M notional in options)

    scenarios = [
        Scenario(
            name="2008 Lehman Liquidity Freeze",
            rates_slope_shock_bps=120.0,
            fx_carry_shock_pct=-0.22,
            equity_spot_shock_pct=-0.35,
            vol_shock_pts=0.30,
        ),
        Scenario(
            name="2020 Covid Flash Crash",
            rates_slope_shock_bps=65.0,
            fx_carry_shock_pct=-0.14,
            equity_spot_shock_pct=-0.28,
            vol_shock_pts=0.45,
        ),
        Scenario(
            name="2022 Fed Hawkish Inflation Shock",
            rates_slope_shock_bps=-110.0,
            fx_carry_shock_pct=0.08,
            equity_spot_shock_pct=-0.18,
            vol_shock_pts=0.06,
        ),
        Scenario(
            name="2024 JPY Carry Trade Unwind",
            rates_slope_shock_bps=30.0,
            fx_carry_shock_pct=-0.16,
            equity_spot_shock_pct=-0.10,
            vol_shock_pts=0.25,
        ),
    ]

    print("=== Macro Portfolio Tail Stress Revaluation ($17M Gross Exposure) ===")
    print(f"{'Scenario Name':<34}{'Non-Linear P&L':<18}{'Linear Approx P&L':<18}{'Convexity Gap':<14}")
    print("-" * 84)

    for sc in scenarios:
        slope_shock = sc.rates_slope_shock_bps
        fx_shock = sc.fx_carry_shock_pct
        eq_shock = sc.equity_spot_shock_pct
        vol_shock = sc.vol_shock_pts

        # 1. Steepener P&L: DV01 of $10M spread is ~$3,500 per bp
        # Slope change in bps * DV01
        pnl_steepener = slope_shock * 3500.0

        # 2. FX Carry P&L: delta-one cash return
        pnl_carry = 5_000_000.0 * fx_shock

        # 3. Equity Option Straddle P&L: Non-linear revaluation vs linear delta
        s0 = 100.0
        s1 = s0 * (1.0 + eq_shock)
        v0 = 0.18
        v1 = v0 + vol_shock
        t = 0.25
        r = 0.045
        nl_call, lin_call = bsm_call_pnl(s0, s1, 100.0, v0, v1, t, r)
        # Put via parity / symmetry
        nl_put, lin_put = bsm_call_pnl(s0, 2 * s0 - s1, 100.0, v0, v1, t, r)
        straddle_nl_pct = (nl_call + nl_put) / 20.0  # Normalized to option budget
        straddle_lin_pct = (lin_call + lin_put) / 20.0

        pnl_straddle_nl = 2_000_000.0 * straddle_nl_pct
        pnl_straddle_lin = 2_000_000.0 * straddle_lin_pct

        total_nonlinear = pnl_steepener + pnl_carry + pnl_straddle_nl
        total_linear = pnl_steepener + pnl_carry + pnl_straddle_lin
        convexity_gap = total_nonlinear - total_linear

        print(f"{sc.name:<34}${total_nonlinear:>12,.0f}     ${total_linear:>12,.0f}     ${convexity_gap:>10,.0f}")


main()
