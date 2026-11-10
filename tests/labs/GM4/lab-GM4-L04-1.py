"""Lab GM4-L04-1: Carry, Roll-Down, and Financing Drag in Fixed Income Expressions.

Decomposes 1-year holding period returns into coupon carry, roll-down along an
upward-sloping yield curve, and repo financing drag across 2Y, 5Y, 10Y, and 30Y tenors.
"""

from __future__ import annotations

import math


def nelson_siegel_yield(maturity: float, b0: float, b1: float, b2: float, lam: float) -> float:
    """Calculate Nelson-Siegel zero yield for given maturity."""
    if maturity <= 0:
        return b0 + b1
    tau = maturity * lam
    factor1 = (1.0 - math.exp(-tau)) / tau
    factor2 = factor1 - math.exp(-tau)
    return b0 + b1 * factor1 + b2 * factor2


def main() -> None:
    # Nelson-Siegel parameters representing a standard upward-sloping yield curve
    b0 = 0.048  # Long-term asymptotic level
    b1 = -0.018  # Short-term component (slope)
    b2 = -0.012  # Curvature
    lam = 0.65  # Decay factor

    repo_rate = 0.035  # General collateral repo financing rate
    horizon_years = 1.0  # 1-year holding period

    tenors = [2.0, 5.0, 10.0, 30.0]
    durations = [1.90, 4.45, 8.10, 17.50]

    print("=== Carry & Roll-Down Attribution (1-Year Horizon, Repo = 3.50%) ===")
    print(f"{'Tenor':<8}{'Init Yield':<12}{'Roll Yield':<12}{'Roll-Down':<12}{'Repo Drag':<12}{'Net Carry':<12}")
    print("-" * 68)

    for m, dur in zip(tenors, durations, strict=True):
        init_yield = nelson_siegel_yield(m, b0, b1, b2, lam)
        rolled_maturity = m - horizon_years
        rolled_yield = nelson_siegel_yield(rolled_maturity, b0, b1, b2, lam)

        # Yield slide along the curve: initial yield minus rolled yield
        roll_down_bps = (init_yield - rolled_yield) * 10_000.0

        # Roll-down price gain = duration * (init_yield - rolled_yield)
        roll_down_gain = dur * (init_yield - rolled_yield)

        gross_carry = init_yield * horizon_years
        repo_drag = repo_rate * horizon_years
        net_carry = gross_carry + roll_down_gain - repo_drag
        net_carry_bps = net_carry * 10_000.0

        print(
            f"{int(m):>2}Y      "
            f"{init_yield * 100:>5.2f}%      "
            f"{rolled_yield * 100:>5.2f}%      "
            f"{roll_down_bps:>6.1f} bps   "
            f"{repo_drag * 100:>5.2f}%      "
            f"{net_carry_bps:>6.1f} bps"
        )


main()
