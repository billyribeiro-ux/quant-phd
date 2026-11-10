"""Lab X3-L02-1: Commodity Futures Term Structure: Backwardation, Contango, and Super-Contango.

Models multi-tenor forward curves across storage regimes, calculates annualized
curve slopes, implied convenience yields, and quantifies Keynesian normal backwardation.
"""

from __future__ import annotations

import math


def generate_curve(spot: float, net_carry: float, tenors_months: list[int]) -> list[float]:
    """Generate futures prices across tenors: F(T) = S * exp(psi * T/12)."""
    return [round(spot * math.exp(net_carry * (t / 12.0)), 2) for t in tenors_months]


def annualized_slope(f1: float, f12: float, dt_years: float = 11.0 / 12.0) -> float:
    """Compute annualized log slope: (ln(F_12) - ln(F_1)) / dt."""
    return (math.log(f12) - math.log(f1)) / dt_years


def implied_convenience_yield(f1: float, f12: float, r: float, c: float, dt_years: float = 11.0 / 12.0) -> float:
    """Compute implied annualized convenience yield delta = r + c - slope."""
    slope = annualized_slope(f1, f12, dt_years)
    return (r + c) - slope


def main() -> None:
    print("Lab X3-L02-1 | Commodity Curve Regimes & Keynes Normal Backwardation")
    print("-" * 75)

    spot = 80.0
    r = 0.04  # 4% risk-free financing
    c = 0.03  # 3% physical storage cost
    tenors = [1, 2, 3, 6, 9, 12]

    # Regimes:
    # 1. Contango (ample inventory: delta = 0.01 < r+c = 0.07 => psi = +0.06)
    # 2. Backwardation (tight inventory: delta = 0.22 > r+c = 0.07 => psi = -0.15)
    # 3. Super-contango (storage collapse / bottleneck: psi = +0.40)
    regimes = {
        "Contango (High Inventory)": 0.06,
        "Backwardation (Tight Supply)": -0.15,
        "Super-Contango (Storage Bottleneck)": 0.40,
    }

    print(f"{'Regime':<35} {'1M':>6} {'3M':>6} {'6M':>6} {'12M':>6} {'Slope p.a.':>11} {'Impl Delta':>11}")
    print("-" * 75)

    for name, psi in regimes.items():
        curve = generate_curve(spot, psi, tenors)
        f1 = curve[0]
        f3 = curve[2]
        f6 = curve[3]
        f12 = curve[5]
        slope = annualized_slope(f1, f12)
        delta = implied_convenience_yield(f1, f12, r, c)
        print(f"{name:<35} {f1:6.2f} {f3:6.2f} {f6:6.2f} {f12:6.2f} {slope * 100:10.2f}% {delta * 100:10.2f}%")

    print("-" * 75)
    print("Keynes (1930) Normal Backwardation vs Price of Storage:")
    # Suppose expected future spot E[S_T] = $80.00 across all regimes (martingale spot)
    exp_spot = 80.0
    for name, psi in regimes.items():
        curve = generate_curve(spot, psi, tenors)
        f12 = curve[5]
        risk_premium = exp_spot - f12
        is_normal_back = f12 < exp_spot
        is_market_back = f12 < spot
        short_name = name.split()[0]
        print(
            f"  {short_name:<16}: F_12M=${f12:6.2f} | E[S_12M]-F_12M = ${risk_premium:6.2f} "
            f"| Normal Back: {is_normal_back!s:<5} | Market Back: {is_market_back!s:<5}"
        )


main()
