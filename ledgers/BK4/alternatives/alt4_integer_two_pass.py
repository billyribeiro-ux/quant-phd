"""Alternative correct implementation 4: integer-only, two passes for the survivors, and an explicit type check."""

from __future__ import annotations

import itertools
from dataclasses import dataclass


@dataclass(frozen=True)
class Waterfall:
    """The result of one default, in cents: the three layers, the survivors' payments and the uncovered loss."""

    margin_cents: int
    default_fund_cents: int
    ccp_capital_cents: int
    survivor_cents: dict[int, int]
    uncovered_cents: int


def _check_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int in cents")
    return value


def waterfall(
    loss_cents: int,
    defaulter_id: int,
    initial_margin_cents: dict[int, int],
    default_fund_cents: dict[int, int],
    ccp_capital_cents: int,
) -> Waterfall:
    """Integer arithmetic only. Pass one floors each share; pass two gives the leftover to positive funds in order."""
    loss = _check_int(loss_cents, "loss_cents")
    capital = _check_int(ccp_capital_cents, "ccp_capital_cents")
    if loss < 0:
        raise ValueError(f"loss_cents is negative, and a loss cannot be negative: {loss}")
    for member, amount in initial_margin_cents.items():
        if _check_int(amount, "initial_margin_cents") < 0:
            raise ValueError(f"initial_margin_cents is negative for member {member}")
    for member, amount in default_fund_cents.items():
        if _check_int(amount, "default_fund_cents") < 0:
            raise ValueError(f"default_fund_cents is negative for member {member}")
    if capital < 0:
        raise ValueError(f"ccp_capital_cents is negative: {capital}")
    if defaulter_id not in default_fund_cents or defaulter_id not in initial_margin_cents:
        raise ValueError(f"defaulter_id {defaulter_id} is not one of the member ids")
    p_margin = min(loss, initial_margin_cents[defaulter_id])
    p_fund = min(loss - p_margin, default_fund_cents[defaulter_id])
    p_capital = min(loss - p_margin - p_fund, capital)
    residual = loss - p_margin - p_fund - p_capital
    others = sorted(m for m in default_fund_cents if m != defaulter_id)
    pool = sum(default_fund_cents[m] for m in others)
    if residual >= pool:
        return Waterfall(p_margin, p_fund, p_capital, {m: default_fund_cents[m] for m in others}, residual - pool)
    floors = {m: (residual * default_fund_cents[m]) // pool for m in others}
    spare = residual - sum(floors.values())
    positive = (m for m in others if default_fund_cents[m] > 0)
    for m in itertools.islice(positive, spare):
        floors[m] += 1
    return Waterfall(p_margin, p_fund, p_capital, floors, 0)


def margin_for_cover(losses_cents: list[int], target_bps: int) -> int:
    """The k-th smallest loss; k is the ceiling of target_bps * S / 10000 written as (x + 9999) // 10000."""
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if not 1 <= target_bps <= 10_000:
        raise ValueError(f"target_bps must be in the range 1 to 10000, not {target_bps}")
    if any(loss < 0 for loss in losses_cents):
        raise ValueError("losses cannot be negative")
    k = (target_bps * len(losses_cents) + 9_999) // 10_000
    ordered = sorted(losses_cents)
    return ordered[k - 1]


def cover_bps(losses_cents: list[int], margin_cents: int) -> int:
    """Floored basis points of scenarios whose loss is at most the margin."""
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if any(loss < 0 for loss in losses_cents):
        raise ValueError("losses cannot be negative")
    count = sum(1 for loss in losses_cents if loss <= margin_cents)
    return count * 10_000 // len(losses_cents)
