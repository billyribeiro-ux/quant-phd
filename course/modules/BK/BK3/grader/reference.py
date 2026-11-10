"""Reference solution for the BK3 project: LDI collateral-spiral model (ldi_model.py).

Implements the Fund and Step dataclasses, the cumulative margin call function,
the closed-form forced-selling threshold, and the multi-step collateral spiral simulator.

Conventions:
- All monetary amounts are non-negative integer cents (int).
- Durations are in hundredths of a year (e.g. 1500 = 15.00 years).
- Rates and yield shocks are in integer basis points.
- Rounding follows the half-up rule: round_half_up(x) = floor(x + 1/2) using exact Fraction arithmetic.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Fund:
    """A defined-benefit pension fund with bond assets and an interest-rate swap overlay.

    All amounts are non-negative integer cents, durations are in hundredths of a year,
    and rates/impacts are in basis points.
    """

    assets_cents: int
    asset_duration_cy: int
    overlay_notional_cents: int
    overlay_duration_cy: int
    buffer_cents: int
    impact_bps_per_gcent: int
    backstop_trigger_bps: int
    backstop_capacity_cents: int

    def __post_init__(self) -> None:
        if self.assets_cents <= 0:
            raise ValueError("assets_cents must be strictly positive")
        if self.asset_duration_cy < 0:
            raise ValueError("asset_duration_cy must be non-negative")
        if self.overlay_notional_cents < 0:
            raise ValueError("overlay_notional_cents must be non-negative")
        if self.overlay_duration_cy < 0:
            raise ValueError("overlay_duration_cy must be non-negative")
        if self.buffer_cents < 0:
            raise ValueError("buffer_cents must be non-negative")
        if self.impact_bps_per_gcent < 0:
            raise ValueError("impact_bps_per_gcent must be non-negative")
        if self.backstop_trigger_bps < 0:
            raise ValueError("backstop_trigger_bps must be non-negative")
        if self.backstop_capacity_cents < 0:
            raise ValueError("backstop_capacity_cents must be non-negative")


@dataclass(frozen=True)
class Step:
    """One iteration of the LDI collateral spiral."""

    step: int
    cumulative_bps: int
    margin_call_cents: int
    buffer_paid_cents: int
    forced_sale_cents: int
    backstop_absorbed_cents: int
    price_impact_bps: int


def _round_half_up(val: Fraction) -> int:
    """Round a non-negative Fraction half up to the nearest integer: floor(val + 1/2)."""
    return math.floor(val + Fraction(1, 2))


def margin_call_cents(fund: Fund, cumulative_bps: int) -> int:
    """Calculate the cumulative variation margin due for a cumulative yield increase of cumulative_bps.

    Formula: Due(Y) = round_half_up(N * D_h * Y / 10^6)
    Raises ValueError if cumulative_bps is negative.
    """
    if cumulative_bps < 0:
        raise ValueError("cumulative_bps must be non-negative")
    exact = Fraction(fund.overlay_notional_cents * fund.overlay_duration_cy * cumulative_bps, 1_000_000)
    return _round_half_up(exact)


def threshold_bps(fund: Fund) -> int | None:
    """Calculate the smallest integer yield shock s >= 0 such that margin_call_cents(fund, s) > fund.buffer_cents.

    Returns None if overlay_notional_cents * overlay_duration_cy == 0.
    """
    prod = fund.overlay_notional_cents * fund.overlay_duration_cy
    if prod == 0:
        return None
    num = (2 * fund.buffer_cents + 1) * 1_000_000
    den = 2 * prod
    return -(-num // den)


def run_steps(fund: Fund, shock_bps: int, backstop: bool) -> list[Step]:
    """Simulate the LDI collateral spiral under an initial yield shock.

    The path terminates when a step produces zero forced sales (S_r == 0),
    zero price impact (I_r == 0), or reaches the cap of 50 steps.
    Raises ValueError if shock_bps is negative.
    """
    if shock_bps < 0:
        raise ValueError("shock_bps must be non-negative")

    steps: list[Step] = []
    remaining_buffer = fund.buffer_cents
    remaining_capacity = fund.backstop_capacity_cents if backstop else 0
    cum_bps = shock_bps
    prev_due = 0

    for step_idx in range(50):
        cum_due = margin_call_cents(fund, cum_bps)
        step_call = cum_due - prev_due
        prev_due = cum_due

        paid = min(step_call, remaining_buffer)
        remaining_buffer -= paid
        forced_sale = step_call - paid

        absorbed = 0
        if backstop and cum_bps >= fund.backstop_trigger_bps:
            absorbed = min(forced_sale, remaining_capacity)
            remaining_capacity -= absorbed

        unabsorbed = forced_sale - absorbed
        exact_impact = Fraction(fund.impact_bps_per_gcent * unabsorbed, 1_000_000_000)
        impact_bps = _round_half_up(exact_impact)

        steps.append(
            Step(
                step=step_idx,
                cumulative_bps=cum_bps,
                margin_call_cents=step_call,
                buffer_paid_cents=paid,
                forced_sale_cents=forced_sale,
                backstop_absorbed_cents=absorbed,
                price_impact_bps=impact_bps,
            )
        )

        if forced_sale == 0 or impact_bps == 0:
            break

        cum_bps += impact_bps

    return steps
