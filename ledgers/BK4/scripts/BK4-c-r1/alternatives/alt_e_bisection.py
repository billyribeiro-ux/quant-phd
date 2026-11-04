"""Alternative E (verifier-written, BK4-c): bisection over integer margins on the cover predicate; no sort."""

from __future__ import annotations

from dataclasses import dataclass


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
    layers = []
    rest = loss_cents
    for cap in (initial_margin_cents[defaulter_id], default_fund_cents[defaulter_id], ccp_capital_cents):
        take = min(rest, cap)
        layers.append(take)
        rest -= take
    survivors = sorted(m for m in default_fund_cents if m != defaulter_id)
    pool = sum(default_fund_cents[m] for m in survivors)
    if rest >= pool:
        return Waterfall(layers[0], layers[1], layers[2], {m: default_fund_cents[m] for m in survivors}, rest - pool)
    paid = {m: rest * default_fund_cents[m] // pool for m in survivors}
    short = rest - sum(paid.values())
    for m in survivors:
        if short > 0 and default_fund_cents[m] > 0:
            paid[m] += 1
            short -= 1
    return Waterfall(layers[0], layers[1], layers[2], paid, 0)


def margin_for_cover(losses_cents: list[int], target_bps: int) -> int:
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if not 1 <= target_bps <= 10_000:
        raise ValueError(f"target_bps must be between 1 and 10000, got {target_bps}")
    if any(x < 0 for x in losses_cents):
        raise ValueError("losses cannot be negative")
    low, high = 0, max(losses_cents)
    while low < high:
        mid = (low + high) // 2
        if cover_bps(losses_cents, mid) >= target_bps:
            high = mid
        else:
            low = mid + 1
    return low


def cover_bps(losses_cents: list[int], margin_cents: int) -> int:
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if any(x < 0 for x in losses_cents):
        raise ValueError("losses cannot be negative")
    return 10_000 * sum(1 for x in losses_cents if x <= margin_cents) // len(losses_cents)
