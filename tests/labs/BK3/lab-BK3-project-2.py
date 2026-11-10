"""BK3 Lab Project-2 (Rung 2 Completion Problem): Sizing margin calls and forced liquidations.

SIMULATED. Illustrative LDI fund parameters, not market data.
The completion problem from Rung 2: replaces blanks with the exact margin call and forced sale expressions.
"""

from __future__ import annotations

import math
from fractions import Fraction


def round_half_up(val: Fraction) -> int:
    return math.floor(val + Fraction(1, 2))


def main() -> None:
    overlay_notional = 120_000_000  # $1,200,000 notional overlay
    overlay_duration_cy = 600  # 6.00 years modified duration
    buffer_cents = 2_000_000  # $20,000 cash buffer
    impact_bps_per_gcent = 2500  # 2500 bps per 10^9 cents sold
    shock_bps = 35  # 35 bps shock

    # Sizing variation margin call using exact Fraction arithmetic
    exact_margin_frac = Fraction(overlay_notional * overlay_duration_cy * shock_bps, 1_000_000)
    margin_call_cents = round_half_up(exact_margin_frac)

    # Cash buffer payment
    buffer_paid_cents = min(margin_call_cents, buffer_cents)

    # Forced asset liquidation after buffer exhaustion
    forced_sale_cents = margin_call_cents - buffer_paid_cents

    # Price impact
    exact_impact_frac = Fraction(impact_bps_per_gcent * forced_sale_cents, 1_000_000_000)
    price_impact_bps = round_half_up(exact_impact_frac)

    print(f"Margin Call:   ${margin_call_cents / 100:,.2f} ({margin_call_cents} cents)")
    print(f"Buffer Paid:   ${buffer_paid_cents / 100:,.2f} ({buffer_paid_cents} cents)")
    print(f"Forced Sale:   ${forced_sale_cents / 100:,.2f} ({forced_sale_cents} cents)")
    print(f"Price Impact:  +{price_impact_bps} bps")


main()
