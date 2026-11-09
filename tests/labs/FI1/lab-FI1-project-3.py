"""Lab FI1-project-3 (Rung 3, Sanity Run): Reference outputs for the Atlas A5 curve engine.

SIMULATED: reference bond portfolio and yield curve parameters for independent validation.
Every student implementation must reproduce these numerical values within stated tolerances.
NumPy and standard library only; no network.
"""

from __future__ import annotations

import datetime
import math
from fractions import Fraction


def day_count(start: datetime.date, end: datetime.date, conv: str) -> Fraction:
    if conv == "ACT/360":
        return Fraction((end - start).days, 360)
    if conv == "ACT/365":
        return Fraction((end - start).days, 365)
    if conv == "30/360":
        d1 = min(start.day, 30)
        d2 = min(end.day, 30)
        days = 360 * (end.year - start.year) + 30 * (end.month - start.month) + (d2 - d1)
        return Fraction(days, 360)
    raise ValueError(f"Unknown convention {conv}")


def price_bond(face: int, coupon: Fraction, periods: int, y: Fraction) -> int:
    v = Fraction(1, 1) / (1 + y)
    vn = v**periods
    annuity = (1 - vn) / y if y != 0 else Fraction(periods)
    unrounded = Fraction(face) * (coupon * annuity + vn)
    return math.floor(unrounded + Fraction(1, 2))


def ns_eval(tau: float, b0: float, b1: float, b2: float, lam: float) -> float:
    x = tau / lam
    g = (1.0 - math.exp(-x)) / x
    return float(b0 + b1 * g + b2 * (g - math.exp(-x)))


def sv_eval(tau: float, b0: float, b1: float, b2: float, b3: float, l1: float, l2: float) -> float:
    ns_part = ns_eval(tau, b0, b1, b2, l1)
    x2 = tau / l2
    g2 = (1.0 - math.exp(-x2)) / x2
    return float(ns_part + b3 * (g2 - math.exp(-x2)))


def main() -> None:
    # 1. Day count reference
    d_start = datetime.date(2024, 1, 15)
    d_end = datetime.date(2024, 7, 15)
    print("Reference Day Count Fractions (2024-01-15 to 2024-07-15):")
    for conv in ("ACT/360", "ACT/365", "30/360"):
        frac = day_count(d_start, d_end, conv)
        print(f"  {conv:7s} = {frac} ({float(frac):.6f})")

    # 2. Bond pricing reference
    face = 100_000
    coupon = Fraction(25, 1000)
    periods = 20
    yield_period = Fraction(225, 10000)
    p_cents = price_bond(face, coupon, periods, yield_period)
    print("\nReference Dirty Price (Face = $1000, 20 periods, c = 2.5%, y = 2.25%):")
    print(f"  Price = ${p_cents / 100:.2f} ({p_cents} cents)")

    # 3. Bootstrapping reference on 4 par bonds (1, 2, 3, 4 periods)
    # Par coupons per period: 1.5%, 1.8%, 2.0%, 2.2%
    par_coupons = [Fraction(15, 1000), Fraction(18, 1000), Fraction(20, 1000), Fraction(22, 1000)]
    dfs: list[Fraction] = [Fraction(1, 1)]
    zero_rates: list[float] = []
    print("\nReference Bootstrapping on 4 Par Bonds:")
    for n, c in enumerate(par_coupons, start=1):
        # Par bond: price_ratio = 1
        df_n = (Fraction(1, 1) - c * sum(dfs[1:n])) / (1 + c)
        dfs.append(df_n)
        zn = float(df_n) ** (-1.0 / n) - 1.0
        zero_rates.append(zn)
        print(f"  Period {n}: DF = {float(df_n):.6f}, Zero Rate = {zn:.6%}")

    # 4. Nelson-Siegel and Svensson reference yields
    b0, b1, b2, b3 = 0.05, -0.02, 0.02, -0.01
    l1, l2 = 2.0, 5.0
    print("\nReference Curve Yields (tau = 1, 2, 5, 10, 30 years):")
    for tau in (1.0, 2.0, 5.0, 10.0, 30.0):
        y_ns = ns_eval(tau, b0, b1, b2, l1)
        y_sv = sv_eval(tau, b0, b1, b2, b3, l1, l2)
        print(f"  tau = {tau:4.1f} yr: NS = {y_ns:.6%}, Svensson = {y_sv:.6%}")


main()
