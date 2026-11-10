"""Lab PM4-L03-1: Negative Convexity and Price Compression of Mortgages.

SIMULATED: Demonstrates price compression, negative convexity, and duration extension
of an agency mortgage pass-through compared to an option-free bullet bond across a wide yield spectrum.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np


def price_bullet_bond(
    coupon_rate: float,
    yield_rate: float,
    maturity_years: float = 10.0,
    face_value: float = 100.0,
    frequency: int = 2,
) -> float:
    """Price an option-free bullet coupon bond."""
    n_periods = int(maturity_years * frequency)
    periodic_c = coupon_rate / frequency
    periodic_y = yield_rate / frequency
    pv_coupons = (face_value * periodic_c) * (1.0 - (1.0 + periodic_y) ** (-n_periods)) / periodic_y
    pv_face = face_value * ((1.0 + periodic_y) ** (-n_periods))
    return float(pv_coupons + pv_face)


def price_mbs_pass_through(
    gross_wac: float,
    net_coupon: float,
    market_yield: float,
    wam_months: int = 360,
    notional: float = 100.0,
) -> float:
    """Price a mortgage pass-through under state-dependent prepayment."""
    wac_m = gross_wac / 12.0
    net_m = net_coupon / 12.0
    disc_m = market_yield / 12.0

    current_balance = notional
    pv = 0.0

    for m in range(1, wam_months + 1):
        if current_balance <= 1e-4:
            break

        rem_term = wam_months - m + 1
        denom = 1.0 - (1.0 + wac_m) ** (-rem_term)
        pmt = current_balance * (wac_m / denom)
        sp = pmt - current_balance * wac_m

        # Refinancing spread incentive: WAC - market yield
        spread = gross_wac - market_yield
        # Prepayment S-curve: base 6% CPR plus surge up to 50% CPR when in the money
        cpr = 0.06 + 0.44 / (1.0 + float(np.exp(-45.0 * (spread - 0.005))))
        smm = 1.0 - (1.0 - cpr) ** (1.0 / 12.0)
        pp = max(0.0, (current_balance - sp) * smm)

        tot_prin = sp + pp
        net_int = current_balance * net_m
        tot_cf = net_int + tot_prin

        # Discount cash flow
        pv += tot_cf / ((1.0 + disc_m) ** m)
        current_balance -= tot_prin

    return float(pv)


def compute_duration_and_convexity(
    pricer_func: Callable[[float], float],
    base_yield: float,
    dy: float = 0.0020,
) -> tuple[float, float, float]:
    """Compute numerical price, effective duration, and effective convexity via finite differences."""
    p0 = float(pricer_func(base_yield))
    p_up = float(pricer_func(base_yield + dy))
    p_down = float(pricer_func(base_yield - dy))

    eff_duration = (p_down - p_up) / (2.0 * p0 * dy)
    eff_convexity = (p_up + p_down - 2.0 * p0) / (p0 * (dy**2))
    return p0, eff_duration, eff_convexity


def main() -> None:
    wac = 0.065
    net_c = 0.060
    bullet_coupon = 0.060
    yields = [0.035, 0.045, 0.055, 0.065, 0.075, 0.085, 0.095]

    print("MBS Pass-Through vs Option-Free Bullet Bond Across Yield Levels:")
    print("Yield (%) | MBS Price | Bullet Price | MBS Eff Dur | Bullet Dur | MBS Convexity | Bullet Cvx")

    mbs_convexities: list[float] = []

    for y in yields:
        p_mbs, d_mbs, c_mbs = compute_duration_and_convexity(
            lambda yld: price_mbs_pass_through(wac, net_c, yld), y, dy=0.0010
        )
        p_bul, d_bul, c_bul = compute_duration_and_convexity(
            lambda yld: price_bullet_bond(bullet_coupon, yld, maturity_years=10.0), y, dy=0.0010
        )
        mbs_convexities.append(c_mbs)
        row = (
            f"{y * 100:9.2f} | {p_mbs:9.2f} | {p_bul:12.2f} | "
            f"{d_mbs:11.2f} | {d_bul:10.2f} | {c_mbs:13.2f} | {c_bul:10.2f}"
        )
        print(row)

    # Validate core theorems of negative convexity
    # 1. MBS price is compressed (capped) near par relative to bullet when rates collapse to 3.5%
    p_mbs_low, _, _ = compute_duration_and_convexity(
        lambda yld: price_mbs_pass_through(wac, net_c, yld), 0.035, dy=0.0010
    )
    p_bul_low, _, _ = compute_duration_and_convexity(
        lambda yld: price_bullet_bond(bullet_coupon, yld, maturity_years=10.0), 0.035, dy=0.0010
    )
    print("\nPrice Compression at 3.50% Yield:")
    print(f"MBS Price:    {p_mbs_low:6.2f}")
    print(f"Bullet Price: {p_bul_low:6.2f}")
    assert p_mbs_low < p_bul_low

    # 2. MBS exhibits negative convexity in the refinancing zone (e.g. 5.5% - 6.5%)
    min_mbs_cvx = min(mbs_convexities)
    print(f"\nMinimum MBS Effective Convexity: {min_mbs_cvx:6.2f}")
    assert min_mbs_cvx < 0.0

    # 3. Bullet bond has positive convexity everywhere
    for y in yields:
        _, _, c_bul = compute_duration_and_convexity(
            lambda yld: price_bullet_bond(bullet_coupon, yld, maturity_years=10.0), y, dy=0.0010
        )
        assert c_bul > 0.0


main()
