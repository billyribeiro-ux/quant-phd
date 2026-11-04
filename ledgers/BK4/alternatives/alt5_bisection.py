"""Alternative correct implementation 5: no sort; a bisection over integer margins on the cover predicate."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Waterfall:
    """The result of one default, in cents: the three layers, the survivors' payments and the uncovered loss."""

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
    """Layers in order, then survivors pro rata by an explicit loop that never sorts the survivors."""
    if loss_cents < 0:
        raise ValueError(f"loss_cents is negative, and a loss cannot be negative: {loss_cents}")
    if any(v < 0 for v in initial_margin_cents.values()):
        raise ValueError("initial_margin_cents is negative for some member")
    if any(v < 0 for v in default_fund_cents.values()):
        raise ValueError("default_fund_cents is negative for some member")
    if ccp_capital_cents < 0:
        raise ValueError(f"ccp_capital_cents is negative: {ccp_capital_cents}")
    if defaulter_id not in default_fund_cents or defaulter_id not in initial_margin_cents:
        raise ValueError(f"defaulter_id {defaulter_id} is not one of the member ids")
    x1 = min(loss_cents, initial_margin_cents[defaulter_id])
    x2 = min(loss_cents - x1, default_fund_cents[defaulter_id])
    x3 = min(loss_cents - x1 - x2, ccp_capital_cents)
    left_over = loss_cents - x1 - x2 - x3
    pool = 0
    for m, fund in default_fund_cents.items():
        if m != defaulter_id:
            pool += fund
    survivors: dict[int, int] = {}
    if left_over >= pool:
        for m, fund in default_fund_cents.items():
            if m != defaulter_id:
                survivors[m] = fund
        return Waterfall(x1, x2, x3, survivors, left_over - pool)
    taken = 0
    for m, fund in default_fund_cents.items():
        if m != defaulter_id:
            survivors[m] = (left_over * fund) // pool
            taken += survivors[m]
    spare = left_over - taken
    for m in sorted(survivors):
        if spare == 0:
            break
        if default_fund_cents[m] > 0:
            survivors[m] += 1
            spare -= 1
    return Waterfall(x1, x2, x3, survivors, 0)


def cover_bps(losses_cents: list[int], margin_cents: int) -> int:
    """Floored basis points of scenarios whose loss is at most the margin."""
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if any(loss < 0 for loss in losses_cents):
        raise ValueError("losses cannot be negative")
    return sum(1 for loss in losses_cents if loss <= margin_cents) * 10_000 // len(losses_cents)


def margin_for_cover(losses_cents: list[int], target_bps: int) -> int:
    """The least integer margin with cover at least target_bps, found by bisection on [0, largest loss]."""
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if not 1 <= target_bps <= 10_000:
        raise ValueError(f"target_bps must be in the range 1 to 10000, not {target_bps}")
    if any(loss < 0 for loss in losses_cents):
        raise ValueError("losses cannot be negative")
    low, high = 0, max(losses_cents)
    while low < high:
        middle = (low + high) // 2
        if cover_bps(losses_cents, middle) >= target_bps:
            high = middle
        else:
            low = middle + 1
    return low
