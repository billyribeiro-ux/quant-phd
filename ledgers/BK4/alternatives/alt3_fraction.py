"""Alternative correct implementation 3: Fraction throughout, with math.floor and math.ceil on exact values."""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Waterfall:
    """The result of one default, in cents: the three layers, the survivors' payments and the uncovered loss."""

    margin_cents: int
    default_fund_cents: int
    ccp_capital_cents: int
    survivor_cents: dict[int, int]
    uncovered_cents: int


def _validate_amounts(loss: int, margins: dict[int, int], funds: dict[int, int], capital: int) -> None:
    if loss < 0:
        raise ValueError(f"loss_cents is negative, and a loss cannot be negative: {loss}")
    if any(value < 0 for value in margins.values()):
        raise ValueError("initial_margin_cents is negative for some member")
    if any(value < 0 for value in funds.values()):
        raise ValueError("default_fund_cents is negative for some member")
    if capital < 0:
        raise ValueError(f"ccp_capital_cents is negative: {capital}")


def waterfall(
    loss_cents: int,
    defaulter_id: int,
    initial_margin_cents: dict[int, int],
    default_fund_cents: dict[int, int],
    ccp_capital_cents: int,
) -> Waterfall:
    """The layers, then survivor shares as the exact floor of Fraction(residual * fund, pool)."""
    _validate_amounts(loss_cents, initial_margin_cents, default_fund_cents, ccp_capital_cents)
    if defaulter_id not in default_fund_cents or defaulter_id not in initial_margin_cents:
        raise ValueError(f"defaulter_id {defaulter_id} is not one of the member ids")
    layer_margin = min(Fraction(loss_cents), Fraction(initial_margin_cents[defaulter_id]))
    layer_fund = min(loss_cents - layer_margin, Fraction(default_fund_cents[defaulter_id]))
    layer_capital = min(loss_cents - layer_margin - layer_fund, Fraction(ccp_capital_cents))
    residual = loss_cents - layer_margin - layer_fund - layer_capital
    survivors = sorted(m for m in default_fund_cents if m != defaulter_id)
    pool = Fraction(sum(default_fund_cents[m] for m in survivors))
    shares: dict[int, int] = {}
    uncovered = 0
    if residual >= pool:
        shares = {m: default_fund_cents[m] for m in survivors}
        uncovered = int(residual - pool)
    else:
        for m in survivors:
            shares[m] = math.floor(Fraction(residual) * default_fund_cents[m] / pool)
        left = int(residual) - sum(shares.values())
        for m in survivors:
            if left > 0 and default_fund_cents[m] > 0:
                shares[m] += 1
                left -= 1
    return Waterfall(int(layer_margin), int(layer_fund), int(layer_capital), shares, uncovered)


def margin_for_cover(losses_cents: list[int], target_bps: int) -> int:
    """The sorted loss at index ceil(Fraction(target_bps * S, 10000)), counted from one."""
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if not 1 <= target_bps <= 10_000:
        raise ValueError(f"target_bps must be in the range 1 to 10000, not {target_bps}")
    if any(loss < 0 for loss in losses_cents):
        raise ValueError("losses cannot be negative")
    index = math.ceil(Fraction(target_bps * len(losses_cents), 10_000))
    return sorted(losses_cents)[index - 1]


def cover_bps(losses_cents: list[int], margin_cents: int) -> int:
    """The floor of Fraction(10000 * covered, S) as an integer."""
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if any(loss < 0 for loss in losses_cents):
        raise ValueError("losses cannot be negative")
    covered = sum(1 for loss in losses_cents if loss <= margin_cents)
    return math.floor(Fraction(10_000 * covered, len(losses_cents)))
