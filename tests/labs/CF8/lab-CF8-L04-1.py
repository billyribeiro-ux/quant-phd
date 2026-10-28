"""CF8 L04 lab 1: revolver availability, minimum-liquidity covenant headroom, the pinch week, and a DSO slip.

SIMULATED: the receipts and disbursements are drawn from random.Random(SEED) in this file, and the commitment, the
covenant threshold and the weekly sales are fixed inputs written here. None is any firm's data.
Units: integer cents throughout. A week is 7 days and the horizon is 13 weeks. Interest is not modelled.
Liquidity at week end is ending cash plus undrawn availability, where availability is commitment less drawn balance.
Headroom is liquidity less the covenant threshold. The DSO slip is computed in Fraction and rounded once, to the nearest
cent, with halves rounded up: the amount is 5 days times weekly sales divided by 7, because daily sales are weekly
sales divided by 7 under the 7-day week.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from fractions import Fraction

HORIZON_WEEKS = 13
SEED = 7
OPENING_CASH = 1_200_000
OPENING_DRAWN = 0
MINIMUM_CASH = 1_000_000
COMMITMENT = 1_200_000
COVENANT_THRESHOLD = 1_800_000
WEEKLY_SALES = 1_234_567
SLIP_DAYS = 5


@dataclass(frozen=True)
class Week:
    """One row of the forecast. Every money field is an int in cents."""

    week: int
    receipts: int
    disbursements: int
    draw: int
    repay: int
    ending_cash: int
    drawn: int
    availability: int
    liquidity: int
    headroom: int
    shortfall: int


def simulate_inputs(seed: int) -> tuple[list[int], list[int]]:
    """Weekly receipts and disbursements in cents for the horizon, from random.Random(seed). SIMULATED."""
    rng = random.Random(seed)
    receipts: list[int] = []
    disbursements: list[int] = []
    for week in range(1, HORIZON_WEEKS + 1):
        slump = -350_000 if 5 <= week <= 8 else 0
        receipts.append(1_000_000 + rng.randint(-150_000, 150_000) + slump)
        disbursements.append(1_020_000 + rng.randint(-120_000, 120_000))
    return receipts, disbursements


def forecast(receipts: list[int], disbursements: list[int], commitment: int) -> list[Week]:
    """Weekly rows in cents. A draw covers the shortfall below minimum cash, capped at availability; a repayment
    sweeps cash above minimum cash to the drawn balance, capped at the balance."""
    cash = OPENING_CASH
    drawn = OPENING_DRAWN
    rows: list[Week] = []
    for week, (receipt, payment) in enumerate(zip(receipts, disbursements, strict=True), start=1):
        before = cash + receipt - payment
        draw = 0
        repay = 0
        if before < MINIMUM_CASH:
            draw = min(MINIMUM_CASH - before, commitment - drawn)
        elif before > MINIMUM_CASH and drawn > 0:
            repay = min(before - MINIMUM_CASH, drawn)
        ending = before + draw - repay
        drawn += draw - repay
        availability = commitment - drawn
        liquidity = ending + availability
        rows.append(
            Week(
                week,
                receipt,
                payment,
                draw,
                repay,
                ending,
                drawn,
                availability,
                liquidity,
                liquidity - COVENANT_THRESHOLD,
                max(0, MINIMUM_CASH - ending),
            )
        )
        cash = ending
    return rows


def half_up(amount: Fraction) -> int:
    """The nearest integer, with halves rounded up, for a non-negative Fraction."""
    return math.floor(amount + Fraction(1, 2))


def pinch_week(rows: list[Week]) -> tuple[int, int]:
    """The week of least headroom (earliest on a tie) and its headroom in cents."""
    best = min(rows, key=lambda row: row.headroom)
    return best.week, best.headroom


def required_commitment(receipts: list[int], disbursements: list[int]) -> int:
    """The smallest commitment with no shortfall: the peak drawn balance when no draw is capped."""
    unconstrained = forecast(receipts, disbursements, commitment=10**12)
    return max([OPENING_DRAWN] + [row.drawn for row in unconstrained])


def main() -> None:
    receipts, disbursements = simulate_inputs(SEED)
    rows = forecast(receipts, disbursements, COMMITMENT)
    print(f"SIMULATED case, seed {SEED}, {HORIZON_WEEKS} weeks, integer cents")
    print(
        f"commitment {COMMITMENT}, minimum cash {MINIMUM_CASH}, covenant threshold {COVENANT_THRESHOLD}, "
        f"opening cash {OPENING_CASH}, opening drawn {OPENING_DRAWN}"
    )
    print("week  draw  repay  ending_cash  drawn  availability  liquidity  headroom  shortfall")
    for row in rows:
        print(
            f"{row.week:>4}  {row.draw:>4}  {row.repay:>5}  {row.ending_cash:>11}  {row.drawn:>5}  "
            f"{row.availability:>12}  {row.liquidity:>9}  {row.headroom:>8}  {row.shortfall:>9}"
        )

    cumulative = 0
    identity_ok = True
    net_ok = True
    for row, receipt, payment in zip(rows, receipts, disbursements, strict=True):
        cumulative += receipt - payment
        identity_ok = identity_ok and row.liquidity == OPENING_CASH - OPENING_DRAWN + COMMITMENT + cumulative
        net_ok = net_ok and row.headroom == row.liquidity - COVENANT_THRESHOLD
    print(f"liquidity equals opening cash less opening drawn, plus commitment, plus cumulative net flow: {identity_ok}")
    print(f"headroom equals liquidity less the covenant threshold in every week: {net_ok}")

    week, headroom = pinch_week(rows)
    print(f"pinch week {week}, headroom {headroom} cents")
    path: list[int] = []
    running = 0
    for receipt, payment in zip(receipts, disbursements, strict=True):
        running += receipt - payment
        path.append(running)
    least_net_week = path.index(min(path)) + 1
    print(f"week of least cumulative net flow {least_net_week}; it is the pinch week: {least_net_week == week}")
    print(
        f"least availability {min(row.availability for row in rows)} cents, in week "
        f"{min(rows, key=lambda row: row.availability).week}"
    )
    print(f"largest weekly shortfall {max(row.shortfall for row in rows)} cents")

    needed = required_commitment(receipts, disbursements)
    at_needed = forecast(receipts, disbursements, needed)
    just_below = forecast(receipts, disbursements, needed - 1)
    print(f"required commitment {needed} cents")
    print(f"no shortfall at the required commitment: {all(row.shortfall == 0 for row in at_needed)}")
    print(f"shortfall one cent below it: {max(row.shortfall for row in just_below)} cents")

    slip = half_up(Fraction(SLIP_DAYS * WEEKLY_SALES, 7))
    slipped = list(receipts)
    slipped[0] -= slip
    shifted = forecast(slipped, disbursements, COMMITMENT)
    liquidity_drop = {base.liquidity - alt.liquidity for base, alt in zip(rows, shifted, strict=True)}
    print(f"DSO slip of {SLIP_DAYS} days on weekly sales {WEEKLY_SALES}: receipts fall by {slip} cents in week 1")
    print(f"liquidity falls by the same amount in every week: {liquidity_drop == {slip}}")
    slipped_week, slipped_headroom = pinch_week(shifted)
    print(f"pinch week after the slip {slipped_week}, headroom {slipped_headroom} cents")
    print(f"pinch week unchanged by the slip: {slipped_week == week}")


main()
