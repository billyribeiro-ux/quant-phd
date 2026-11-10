"""BK3 Lab Project-1 (Rung 1 Worked Example): Single-step LDI margin call and forced sale.

SIMULATED. Illustrative LDI fund parameters, not market data.
A fully solved, annotated worked example of a single margin call, cash buffer exhaustion,
and initial forced liquidation under a sovereign bond yield shock.
"""

from __future__ import annotations

import math
from fractions import Fraction


def round_half_up(val: Fraction) -> int:
    """Round Fraction half up to nearest integer."""
    return math.floor(val + Fraction(1, 2))


def main() -> None:
    # 1. Fund parameters (all in integer cents or basis points)
    overlay_notional = 100_000_000  # $1,000,000 notional overlay
    overlay_duration_cy = 500  # 5.00 years modified duration (500 hundredths of a year)
    buffer_cents = 1_000_000  # $10,000 liquid cash buffer held at clearing broker
    impact_bps_per_gcent = 2000  # 2000 bps price impact per 10^9 cents ($10M) liquidated
    shock_bps = 25  # 25 basis points parallel upward shift in sovereign yields

    print("=== Rung 1 Worked Example: Single-Step LDI Margin Call ===")
    print(f"Overlay Notional:       ${overlay_notional / 100:,.2f} cents ({overlay_notional:,} cents)")
    print(f"Overlay Duration:       {overlay_duration_cy / 100:.2f} years ({overlay_duration_cy} hundredths)")
    print(f"Available Cash Buffer:  ${buffer_cents / 100:,.2f} cents ({buffer_cents:,} cents)")
    print(f"Yield Shock:            +{shock_bps} bps")

    # 2. Sizing the variation margin call
    # Formula: Due(Y) = round_half_up(N * D_h * Y / 10^6)
    exact_margin_frac = Fraction(overlay_notional * overlay_duration_cy * shock_bps, 1_000_000)
    margin_call_cents = round_half_up(exact_margin_frac)
    print(f"\nStep 1: Margin Call Due: ${margin_call_cents / 100:,.2f} ({margin_call_cents:,} cents)")

    # 3. Liquid buffer payment
    buffer_paid_cents = min(margin_call_cents, buffer_cents)
    remaining_buffer_cents = buffer_cents - buffer_paid_cents
    print(f"Step 2: Buffer Cash Paid: ${buffer_paid_cents / 100:,.2f} ({buffer_paid_cents:,} cents)")
    print(f"        Remaining Buffer: ${remaining_buffer_cents / 100:,.2f} ({remaining_buffer_cents:,} cents)")

    # 4. Forced asset liquidation
    forced_sale_cents = margin_call_cents - buffer_paid_cents
    print(f"Step 3: Forced Sale:      ${forced_sale_cents / 100:,.2f} ({forced_sale_cents:,} cents)")

    # 5. Price impact
    exact_impact_frac = Fraction(impact_bps_per_gcent * forced_sale_cents, 1_000_000_000)
    price_impact_bps = round_half_up(exact_impact_frac)
    print(f"Step 4: Endogenous Price Impact: +{price_impact_bps} bps (from selling ${forced_sale_cents / 100:,.2f})")

    # Conservation checks
    assert margin_call_cents == buffer_paid_cents + forced_sale_cents, "Cash paid + forced sale must equal margin call"
    print("\nConservation Check: Margin Call == Buffer Paid + Forced Sale -> True")


main()
