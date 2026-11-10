"""Lab PM3-L01-1: Direct Lending All-In Yield and Contractual Return Sensitivity.

SIMULATED: Models floating-rate direct loans across SOFR rate regimes, quantifying the
impact of reference rate floors, original issue discounts (OID), and credit loss provisions.
"""

from __future__ import annotations

import numpy as np


def compute_all_in_yield(
    sofr: float,
    spread: float,
    floor: float,
    oid: float,
    wal: float,
) -> float:
    """Calculate the annualized all-in yield of a floating-rate direct loan.

    Parameters
    ----------
    sofr : float
        Current 3-month term SOFR benchmark rate (decimal, e.g. 0.04 for 4%).
    spread : float
        Contractual credit spread over benchmark (decimal, e.g. 0.06 for 600 bps).
    floor : float
        Contractual benchmark rate floor (decimal, e.g. 0.01 for 100 bps).
    oid : float
        Original issue discount percentage (decimal, e.g. 0.02 for 2 points / 98 price).
    wal : float
        Weighted average life of the loan facility in years.

    Returns
    -------
    float
        Annualized all-in yield as a decimal.
    """
    effective_base = max(sofr, floor)
    cash_coupon = effective_base + spread
    purchase_price = 1.0 - oid
    annualized_oid_amortization = oid / wal
    return float((cash_coupon + annualized_oid_amortization) / purchase_price)


def compute_net_expected_return(
    all_in_yield: float,
    annual_default_prob: float,
    loss_given_default: float,
) -> float:
    """Compute the net expected return after subtracting credit losses.

    Parameters
    ----------
    all_in_yield : float
        Annualized all-in yield as a decimal.
    annual_default_prob : float
        Annual default probability lambda (decimal).
    loss_given_default : float
        Loss given default (1 - recovery rate) as a decimal.

    Returns
    -------
    float
        Net expected annualized return as a decimal.
    """
    expected_loss = annual_default_prob * loss_given_default
    return float(all_in_yield - expected_loss)


def main() -> None:
    spread = 0.060  # 600 bps
    floor = 0.010  # 100 bps floor
    oid = 0.020  # 2.0% OID (issued at 98)
    wal = 3.0  # 3-year weighted average life
    annual_pd = 0.025  # 2.5% annual default probability
    lgd = 0.35  # 35% loss given default (65% recovery)

    sofr_scenarios = [0.000, 0.005, 0.010, 0.020, 0.030, 0.040, 0.050, 0.060]

    print("Direct Lending All-In Yield & Net Return Matrix:")
    print("SOFR (%) | Effective Base (%) | All-In Yield (%) | Expected Loss (%) | Net Return (%)")
    print("-" * 85)

    for r in sofr_scenarios:
        eff_base = max(r, floor)
        y_all = compute_all_in_yield(r, spread, floor, oid, wal)
        exp_loss = annual_pd * lgd
        net_ret = compute_net_expected_return(y_all, annual_pd, lgd)
        print(
            f"{r * 100:8.2f} | {eff_base * 100:18.2f} | {y_all * 100:16.4f} | "
            f"{exp_loss * 100:17.4f} | {net_ret * 100:14.4f}"
        )

    # Floor protection analysis at zero SOFR vs 50 bps SOFR
    y_zero = compute_all_in_yield(0.000, spread, floor, oid, wal)
    y_50bp = compute_all_in_yield(0.005, spread, floor, oid, wal)
    y_floor = compute_all_in_yield(0.010, spread, floor, oid, wal)

    # Both zero and 50 bps must bind to the 1.0% floor
    assert np.isclose(y_zero, y_floor, atol=1e-8)
    assert np.isclose(y_50bp, y_floor, atol=1e-8)

    # Yield at 5.0% SOFR
    y_5pct = compute_all_in_yield(0.050, spread, floor, oid, wal)
    assert y_5pct > y_floor
    print("\nFloor Protection Assertion: Verified binding floor at SOFR <= 1.0%.")
    print(f"Incremental yield from 1% to 5% SOFR: {(y_5pct - y_floor) * 100:.4f} percentage points.")


main()
