"""CF8 L03 lab 1: a SIMULATED 13-week direct cash-flow forecast with a revolving credit facility.

SIMULATED: the weekly receipts and disbursements are drawn from random.Random(SEED) in this file. They are not any
firm's data, and the case is one draw, not a forecast of a real company.
Units: integer cents throughout. A week is 7 days, the horizon is 13 weeks, and week w ends on day 7w.
Every input is an integer number of cents and the forecast uses integer arithmetic only, so no rounding occurs.
Revolver rule: when cash before any draw or repayment is below minimum cash, the revolver draws the
shortfall, capped at undrawn availability. When cash before any repayment is above minimum cash and the
drawn balance is positive, the revolver repays the excess, capped at the drawn balance. Revolver interest
is not modelled in this lab.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

HORIZON_WEEKS = 13
SEED = 7
OPENING_CASH = 1_200_000
OPENING_DRAWN = 0
MINIMUM_CASH = 1_000_000
COMMITMENT = 4_000_000


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


def forecast(
    receipts: list[int],
    disbursements: list[int],
    opening_cash: int,
    opening_drawn: int,
    minimum: int,
    commitment: int,
) -> list[Week]:
    """Weekly rows of the direct forecast in cents, applying the revolver rule in the module docstring."""
    cash = opening_cash
    drawn = opening_drawn
    rows: list[Week] = []
    for week, (receipt, payment) in enumerate(zip(receipts, disbursements, strict=True), start=1):
        before = cash + receipt - payment
        draw = 0
        repay = 0
        if before < minimum:
            draw = min(minimum - before, commitment - drawn)
        elif before > minimum and drawn > 0:
            repay = min(before - minimum, drawn)
        ending = before + draw - repay
        drawn += draw - repay
        rows.append(Week(week, receipt, payment, draw, repay, ending, drawn, max(0, minimum - ending)))
        cash = ending
    return rows


def identity_holds(rows: list[Week], opening_cash: int, receipts: list[int], disbursements: list[int]) -> bool:
    """True when each week's ending cash equals the prior ending cash, plus receipts, less disbursements,
    plus the draw, less the repayment."""
    previous = opening_cash
    for row, receipt, payment in zip(rows, receipts, disbursements, strict=True):
        if row.ending_cash != previous + receipt - payment + row.draw - row.repay:
            return False
        previous = row.ending_cash
    return True


def main() -> None:
    receipts, disbursements = simulate_inputs(SEED)
    rows = forecast(receipts, disbursements, OPENING_CASH, OPENING_DRAWN, MINIMUM_CASH, COMMITMENT)
    print(f"SIMULATED case, seed {SEED}, {HORIZON_WEEKS} weeks, integer cents")
    print(
        f"opening cash {OPENING_CASH}, opening drawn {OPENING_DRAWN}, "
        f"minimum cash {MINIMUM_CASH}, commitment {COMMITMENT}"
    )
    print("week  receipts  disbursements  draw  repay  ending_cash  drawn  shortfall")
    for row in rows:
        print(
            f"{row.week:>4}  {row.receipts:>8}  {row.disbursements:>13}  {row.draw:>4}  {row.repay:>5}  "
            f"{row.ending_cash:>11}  {row.drawn:>5}  {row.shortfall:>9}"
        )
    print(f"cash identity holds in every week: {identity_holds(rows, OPENING_CASH, receipts, disbursements)}")
    print(f"minimum cash held in every week: {all(row.shortfall == 0 for row in rows)}")
    print(
        f"weeks with a draw: {sum(1 for row in rows if row.draw > 0)}; weeks with a repayment: "
        f"{sum(1 for row in rows if row.repay > 0)}"
    )
    print(f"total drawn {sum(row.draw for row in rows)}; total repaid {sum(row.repay for row in rows)}")
    print(
        f"peak drawn balance {max(row.drawn for row in rows)}; least availability "
        f"{COMMITMENT - max(row.drawn for row in rows)}"
    )
    closing = (
        OPENING_CASH
        + sum(receipts)
        - sum(disbursements)
        + sum(row.draw for row in rows)
        - sum(row.repay for row in rows)
    )
    print(f"closing cash from the summed identity {closing}; from the last week {rows[-1].ending_cash}")


main()
