"""Alternative C (verifier-written, BK4-c): Fraction throughout; ceil of the exact target, floor of the exact share."""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Waterfall:
    margin_cents: int
    default_fund_cents: int
    ccp_capital_cents: int
    survivor_cents: dict[int, int]
    uncovered_cents: int


def waterfall(
    loss_cents: int,
    defaulter_id: int,
    initial_margin_cents: dict[int, int],
    default_fund_cents: dict[int, int],
    ccp_capital_cents: int,
) -> Waterfall:
    if loss_cents < 0:
        raise ValueError(f"loss_cents is negative: {loss_cents}")
    for member, amount in initial_margin_cents.items():
        if amount < 0:
            raise ValueError(f"initial_margin_cents is negative for member {member}")
    for member, amount in default_fund_cents.items():
        if amount < 0:
            raise ValueError(f"default_fund_cents is negative for member {member}")
    if ccp_capital_cents < 0:
        raise ValueError(f"ccp_capital_cents is negative: {ccp_capital_cents}")
    if defaulter_id not in default_fund_cents or defaulter_id not in initial_margin_cents:
        raise ValueError(f"defaulter_id {defaulter_id} is not one of the member ids")
    loss = Fraction(loss_cents)
    layer_margin = min(loss, Fraction(initial_margin_cents[defaulter_id]))
    layer_fund = min(loss - layer_margin, Fraction(default_fund_cents[defaulter_id]))
    layer_capital = min(loss - layer_margin - layer_fund, Fraction(ccp_capital_cents))
    residual = loss - layer_margin - layer_fund - layer_capital
    survivors = sorted(m for m in default_fund_cents if m != defaulter_id)
    pool = Fraction(sum(default_fund_cents[m] for m in survivors))
    if residual >= pool:
        paid = {m: default_fund_cents[m] for m in survivors}
        return Waterfall(int(layer_margin), int(layer_fund), int(layer_capital), paid, int(residual - pool))
    paid = {m: math.floor(residual * Fraction(default_fund_cents[m]) / pool) for m in survivors}
    left = int(residual) - sum(paid.values())
    for m in survivors:
        if left > 0 and default_fund_cents[m] > 0:
            paid[m] += 1
            left -= 1
    return Waterfall(int(layer_margin), int(layer_fund), int(layer_capital), {m: int(v) for m, v in paid.items()}, 0)


def margin_for_cover(losses_cents: list[int], target_bps: int) -> int:
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if not 1 <= target_bps <= 10_000:
        raise ValueError(f"target_bps must be in 1 to 10000: {target_bps}")
    if any(x < 0 for x in losses_cents):
        raise ValueError("losses cannot be negative")
    index = math.ceil(Fraction(target_bps * len(losses_cents), 10_000))
    return sorted(losses_cents)[int(index) - 1]


def cover_bps(losses_cents: list[int], margin_cents: int) -> int:
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if any(x < 0 for x in losses_cents):
        raise ValueError("losses cannot be negative")
    share = Fraction(10_000 * sum(1 for x in losses_cents if x <= margin_cents), len(losses_cents))
    return math.floor(share)
