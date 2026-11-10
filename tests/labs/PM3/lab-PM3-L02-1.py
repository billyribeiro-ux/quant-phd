"""Lab PM3-L02-1: Unitranche Agreement Among Lenders (AAL) Waterfall and Subordination.

SIMULATED: Models a bifurcated unitranche loan facility under an Agreement Among Lenders (AAL),
evaluating cash flow distributions and principal recovery waterfalls across distress outcomes.
"""

from __future__ import annotations

import numpy as np


def unitranche_blended_coupon(
    share_fo: float,
    spread_fo: float,
    spread_lo: float,
    sofr: float = 0.05,
) -> tuple[float, float, float]:
    """Compute the blended borrower coupon and tranche coupons.

    Parameters
    ----------
    share_fo : float
        Principal fraction in First-Out tranche (e.g. 0.60 for 60%).
    spread_fo : float
        First-Out credit spread (decimal, e.g. 0.035 for 350 bps).
    spread_lo : float
        Last-Out credit spread (decimal, e.g. 0.085 for 850 bps).
    sofr : float
        Reference SOFR rate (decimal).

    Returns
    -------
    tuple[float, float, float]
        (blended_coupon, coupon_fo, coupon_lo)
    """
    share_lo = 1.0 - share_fo
    coupon_fo = sofr + spread_fo
    coupon_lo = sofr + spread_lo
    blended_coupon = share_fo * coupon_fo + share_lo * coupon_lo
    return blended_coupon, coupon_fo, coupon_lo


def aal_liquidation_waterfall(
    enterprise_recovery: float,
    principal_fo: float,
    principal_lo: float,
) -> tuple[float, float, float, float]:
    """Distribute enterprise liquidation proceeds under an Agreement Among Lenders (AAL).

    Parameters
    ----------
    enterprise_recovery : float
        Total enterprise value available for loan recovery ($).
    principal_fo : float
        First-Out tranche outstanding principal ($).
    principal_lo : float
        Last-Out tranche outstanding principal ($).

    Returns
    -------
    tuple[float, float, float, float]
        (recovery_fo, recovery_lo, rec_rate_fo, rec_rate_lo)
    """
    recovery_fo = min(enterprise_recovery, principal_fo)
    remaining_value = max(0.0, enterprise_recovery - principal_fo)
    recovery_lo = min(remaining_value, principal_lo)

    rec_rate_fo = recovery_fo / principal_fo if principal_fo > 0 else 0.0
    rec_rate_lo = recovery_lo / principal_lo if principal_lo > 0 else 0.0

    return recovery_fo, recovery_lo, rec_rate_fo, rec_rate_lo


def main() -> None:
    principal_total = 100_000_000.0  # $100M total facility
    share_fo = 0.60  # 60% First-Out ($60M)
    principal_fo = principal_total * share_fo
    principal_lo = principal_total * (1.0 - share_fo)  # 40% Last-Out ($40M)

    spread_fo = 0.0350  # SOFR + 350 bps
    spread_lo = 0.0850  # SOFR + 850 bps
    sofr = 0.0500  # 5.0% base rate

    blended, c_fo, c_lo = unitranche_blended_coupon(share_fo, spread_fo, spread_lo, sofr)

    print("Unitranche Facility Capital Structure & Coupon Economics:")
    print(f"Total Facility Principal:      ${principal_total / 1e6:8.2f}M")
    print(f"First-Out (FO) Principal:      ${principal_fo / 1e6:8.2f}M ({share_fo * 100:.1f}%)")
    print(f"Last-Out (LO) Principal:       ${principal_lo / 1e6:8.2f}M ({(1.0 - share_fo) * 100:.1f}%)")
    print(f"FO Coupon (SOFR + 350 bps):    {c_fo * 100:8.2f}%")
    print(f"LO Coupon (SOFR + 850 bps):    {c_lo * 100:8.2f}%")
    print(f"Blended Borrower Coupon:       {blended * 100:8.2f}% (Spread = {(blended - sofr) * 10000:.0f} bps)")

    print("\nAAL Liquidation Waterfall across Enterprise Distress Scenarios:")
    print("Enterprise Rec ($M) | FO Rec ($M) | LO Rec ($M) | FO Rec Rate (%) | LO Rec Rate (%)")
    print("-" * 80)

    recovery_scenarios = [20.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0]
    for ev in recovery_scenarios:
        ev_dollars = ev * 1e6
        r_fo, r_lo, rate_fo, rate_lo = aal_liquidation_waterfall(ev_dollars, principal_fo, principal_lo)
        print(f"{ev:19.1f} | {r_fo / 1e6:11.2f} | {r_lo / 1e6:11.2f} | {rate_fo * 100:15.2f} | {rate_lo * 100:15.2f}")

    # Invariant assertions
    # 1. At $60M EV recovery, FO is 100% recovered and LO is 0% recovered
    _, _, rate_fo_60, rate_lo_60 = aal_liquidation_waterfall(60e6, principal_fo, principal_lo)
    assert np.isclose(rate_fo_60, 1.0)
    assert np.isclose(rate_lo_60, 0.0)

    # 2. At $80M EV recovery, LO recovery is exactly 50% ($20M of $40M)
    _, _, rate_fo_80, rate_lo_80 = aal_liquidation_waterfall(80e6, principal_fo, principal_lo)
    assert np.isclose(rate_fo_80, 1.0)
    assert np.isclose(rate_lo_80, 0.50)

    print("\nWaterfall Priority Assertion: Verified First-Out senior claim and complete Last-Out subordination.")


main()
