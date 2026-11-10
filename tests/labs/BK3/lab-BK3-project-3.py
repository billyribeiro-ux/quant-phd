"""BK3 Lab Project-3 (Rung 3 Independent Verification): Default instance spiral benchmark.

SIMULATED. Illustrative LDI fund benchmark, not market data.
Executes the reference simulator on the default instance parameters (Seed 0).
Prints the exact threshold shock and full spiral simulation tables with and without
a central-bank liquidity backstop that the learner's ldi_model.py implementation must reproduce.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Fund:
    assets_cents: int
    asset_duration_cy: int
    overlay_notional_cents: int
    overlay_duration_cy: int
    buffer_cents: int
    impact_bps_per_gcent: int
    backstop_trigger_bps: int
    backstop_capacity_cents: int


@dataclass(frozen=True)
class Step:
    step: int
    cumulative_bps: int
    margin_call_cents: int
    buffer_paid_cents: int
    forced_sale_cents: int
    backstop_absorbed_cents: int
    price_impact_bps: int


def _round_half_up(val: Fraction) -> int:
    return math.floor(val + Fraction(1, 2))


def margin_call_cents(fund: Fund, cumulative_bps: int) -> int:
    exact = Fraction(fund.overlay_notional_cents * fund.overlay_duration_cy * cumulative_bps, 1_000_000)
    return _round_half_up(exact)


def threshold_bps(fund: Fund) -> int | None:
    prod = fund.overlay_notional_cents * fund.overlay_duration_cy
    if prod == 0:
        return None
    num = (2 * fund.buffer_cents + 1) * 1_000_000
    den = 2 * prod
    return -(-num // den)


def run_steps(fund: Fund, shock_bps: int, backstop: bool) -> list[Step]:
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


def main() -> None:
    # Baseline default instance (Seed 0 parameters from instance.py)
    fund = Fund(
        assets_cents=1_643_341_330,
        asset_duration_cy=953,
        overlay_notional_cents=635_486_061,
        overlay_duration_cy=1861,
        buffer_cents=14_185_179,
        impact_bps_per_gcent=1268,
        backstop_trigger_bps=45,
        backstop_capacity_cents=20_805_175,
    )
    initial_shock = 65  # Seed 0 initial shock

    s_star = threshold_bps(fund)
    print("=== Benchmark Simulation: Default Instance (Seed 0) ===")
    print(f"Threshold Shock s*: {s_star} bps")

    steps_no = run_steps(fund, initial_shock, backstop=False)
    print(f"\nPath 1 (Without Backstop) - {len(steps_no)} steps:")
    for s in steps_no:
        print(
            f"  Step {s.step}: Yield={s.cumulative_bps} bps | Call={s.margin_call_cents:,} | "
            f"BufferPaid={s.buffer_paid_cents:,} | Sale={s.forced_sale_cents:,} | Impact=+{s.price_impact_bps} bps"
        )

    steps_yes = run_steps(fund, initial_shock, backstop=True)
    print(f"\nPath 2 (With Backstop) - {len(steps_yes)} steps:")
    for s in steps_yes:
        print(
            f"  Step {s.step}: Yield={s.cumulative_bps} bps | Call={s.margin_call_cents:,} | "
            f"BufferPaid={s.buffer_paid_cents:,} | Sale={s.forced_sale_cents:,} | "
            f"Absorbed={s.backstop_absorbed_cents:,} | Impact=+{s.price_impact_bps} bps"
        )


main()
