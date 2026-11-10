"""BK3 Lab L06: The LDI Collateral Spiral and Central-Bank Backstop.

SIMULATED. Illustrative LDI fund parameters, not market data.
Simulates a leveraged LDI fund with interest-rate swap overlay facing a sharp rise in sovereign bond yields.
Calculates the forced-selling threshold s* in closed form and checks it against discrete evaluation.
Traces the multi-step collateral spiral:
  - Yield shock triggers variation margin call: Due(Y) = round_half_up(N * D_h * Y / 10^6)
  - Fund exhausts cash buffer; unpaid calls trigger forced asset sales: S_r = M_r - P_r
  - Unabsorbed sales create endogenous price impact: I_r = round_half_up(lambda * S_unabsorbed / 10^9) bps
  - Higher yields provoke subsequent margin calls in a cascading loop.
Compares the spiral trajectory with and without a central-bank liquidity backstop.
All amounts are exact in integer cents.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class FundConfig:
    overlay_notional_cents: int
    overlay_duration_cy: int
    buffer_cents: int
    impact_bps_per_gcent: int
    backstop_trigger_bps: int
    backstop_capacity_cents: int


@dataclass(frozen=True)
class StepRecord:
    step: int
    cumulative_bps: int
    margin_call_cents: int
    buffer_paid_cents: int
    forced_sale_cents: int
    absorbed_cents: int
    impact_bps: int


def _round_half_up(val: Fraction) -> int:
    return math.floor(val + Fraction(1, 2))


def margin_call(fund: FundConfig, cumulative_bps: int) -> int:
    exact = Fraction(fund.overlay_notional_cents * fund.overlay_duration_cy * cumulative_bps, 1_000_000)
    return _round_half_up(exact)


def threshold_closed_form(fund: FundConfig) -> int:
    num = (2 * fund.buffer_cents + 1) * 1_000_000
    den = 2 * fund.overlay_notional_cents * fund.overlay_duration_cy
    return -(-num // den)


def simulate_spiral(fund: FundConfig, initial_shock_bps: int, use_backstop: bool) -> list[StepRecord]:
    steps: list[StepRecord] = []
    rem_buffer = fund.buffer_cents
    rem_capacity = fund.backstop_capacity_cents if use_backstop else 0
    cum_bps = initial_shock_bps
    prev_due = 0

    for step_idx in range(50):
        cum_due = margin_call(fund, cum_bps)
        step_call = cum_due - prev_due
        prev_due = cum_due

        paid = min(step_call, rem_buffer)
        rem_buffer -= paid
        forced_sale = step_call - paid

        absorbed = 0
        if use_backstop and cum_bps >= fund.backstop_trigger_bps:
            absorbed = min(forced_sale, rem_capacity)
            rem_capacity -= absorbed

        unabsorbed = forced_sale - absorbed
        impact = _round_half_up(Fraction(fund.impact_bps_per_gcent * unabsorbed, 1_000_000_000))

        steps.append(
            StepRecord(
                step=step_idx,
                cumulative_bps=cum_bps,
                margin_call_cents=step_call,
                buffer_paid_cents=paid,
                forced_sale_cents=forced_sale,
                absorbed_cents=absorbed,
                impact_bps=impact,
            )
        )

        if forced_sale == 0 or impact == 0:
            break
        cum_bps += impact

    return steps


def main() -> None:
    fund = FundConfig(
        overlay_notional_cents=500_000_000,  # $5,000,000 notional
        overlay_duration_cy=1500,  # 15.00 years
        buffer_cents=10_000_000,  # $100,000 cash buffer
        impact_bps_per_gcent=1500,  # 1500 bps per $10M sold
        backstop_trigger_bps=50,  # Backstop triggers at +50 bps
        backstop_capacity_cents=15_000_000,  # $150,000 intervention capacity
    )

    s_star = threshold_closed_form(fund)
    print("=== LDI Collateral Spiral: Forced-Selling Threshold ===")
    print(f"Overlay Notional: ${fund.overlay_notional_cents / 100:,.2f}")
    print(f"Overlay Duration: {fund.overlay_duration_cy / 100:.2f} years")
    print(f"Liquid Buffer:    ${fund.buffer_cents / 100:,.2f}")
    print(f"Threshold Shock:  s* = {s_star} bps")
    call_below = margin_call(fund, s_star - 1)
    call_at = margin_call(fund, s_star)
    print(f"Margin call at {s_star - 1} bps: ${call_below / 100:,.2f} <= Buffer (${fund.buffer_cents / 100:,.2f})")
    print(f"Margin call at {s_star} bps:     ${call_at / 100:,.2f} > Buffer (${fund.buffer_cents / 100:,.2f})\n")

    initial_shock = 60  # Initial yield shock exceeds threshold
    steps_unhedged = simulate_spiral(fund, initial_shock, use_backstop=False)
    steps_backstopped = simulate_spiral(fund, initial_shock, use_backstop=True)

    print(f"=== Simulation 1: Spiral WITHOUT Backstop (Initial Shock = {initial_shock} bps) ===")
    hdr1 = (
        f"{'Step':<5} | {'Yield (bps)':<12} | {'Margin Call':<14} | "
        f"{'Buffer Paid':<14} | {'Forced Sale':<14} | {'Price Impact'}"
    )
    print(hdr1)
    print("-" * len(hdr1))
    for s in steps_unhedged:
        print(
            f"{s.step:<5} | {s.cumulative_bps:<12} | ${s.margin_call_cents / 100:<13,.2f} | "
            f"${s.buffer_paid_cents / 100:<13,.2f} | ${s.forced_sale_cents / 100:<13,.2f} | +{s.impact_bps} bps"
        )

    print(f"\n=== Simulation 2: Spiral WITH Backstop (Trigger = {fund.backstop_trigger_bps} bps) ===")
    hdr2 = (
        f"{'Step':<5} | {'Yield (bps)':<12} | {'Margin Call':<14} | "
        f"{'Buffer Paid':<14} | {'Forced Sale':<14} | {'Absorbed':<12} | {'Price Impact'}"
    )
    print(hdr2)
    print("-" * len(hdr2))
    for s in steps_backstopped:
        print(
            f"{s.step:<5} | {s.cumulative_bps:<12} | ${s.margin_call_cents / 100:<13,.2f} | "
            f"${s.buffer_paid_cents / 100:<13,.2f} | ${s.forced_sale_cents / 100:<13,.2f} | "
            f"${s.absorbed_cents / 100:<11,.2f} | +{s.impact_bps} bps"
        )

    tot_forced_1 = sum(s.forced_sale_cents for s in steps_unhedged)
    tot_forced_2 = sum(s.forced_sale_cents for s in steps_backstopped)
    final_yield_1 = steps_unhedged[-1].cumulative_bps + steps_unhedged[-1].impact_bps
    final_yield_2 = steps_backstopped[-1].cumulative_bps + steps_backstopped[-1].impact_bps

    print("\n=== Spiral Comparison Summary ===")
    print(
        f"Without backstop: {len(steps_unhedged)} steps | "
        f"Forced Sales: ${tot_forced_1 / 100:,.2f} | Final Shock: +{final_yield_1} bps"
    )
    print(
        f"With backstop:    {len(steps_backstopped)} steps | "
        f"Forced Sales: ${tot_forced_2 / 100:,.2f} | Final Shock: +{final_yield_2} bps"
    )
    print(f"Backstop halted the spiral earlier: {len(steps_backstopped) < len(steps_unhedged)}")


main()
