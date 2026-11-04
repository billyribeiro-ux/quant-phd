"""Alternative D (verifier-written, BK4-c): integer-only; ceiling division; sizing by counting, with no sort."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Waterfall:
    margin_cents: int
    default_fund_cents: int
    ccp_capital_cents: int
    survivor_cents: dict[int, int]
    uncovered_cents: int


def _ceil_div(x: int, y: int) -> int:
    return -((-x) // y)


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
    margin_paid = min(loss_cents, initial_margin_cents[defaulter_id])
    fund_paid = min(loss_cents - margin_paid, default_fund_cents[defaulter_id])
    capital_paid = min(loss_cents - margin_paid - fund_paid, ccp_capital_cents)
    residual = loss_cents - margin_paid - fund_paid - capital_paid
    survivors = [m for m in default_fund_cents if m != defaulter_id]
    pool = 0
    for m in survivors:
        pool += default_fund_cents[m]
    if residual >= pool:
        return Waterfall(margin_paid, fund_paid, capital_paid, {m: default_fund_cents[m] for m in survivors}, residual - pool)
    paid: dict[int, int] = {}
    for m in survivors:
        paid[m] = (residual * default_fund_cents[m]) // pool
    leftover = residual - sum(paid.values())
    for m in sorted(survivors):
        if default_fund_cents[m] == 0:
            continue
        if leftover == 0:
            break
        paid[m] += 1
        leftover -= 1
    return Waterfall(margin_paid, fund_paid, capital_paid, paid, 0)


def margin_for_cover(losses_cents: list[int], target_bps: int) -> int:
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if not 1 <= target_bps <= 10_000:
        raise ValueError(f"target_bps is outside 1 to 10000: {target_bps}")
    if any(x < 0 for x in losses_cents):
        raise ValueError("losses cannot be negative")
    need = _ceil_div(target_bps * len(losses_cents), 10_000)
    # The margin is the smallest loss x whose count of losses at or below x reaches the needed count.
    best: int | None = None
    for x in losses_cents:
        at_or_below = 0
        for y in losses_cents:
            if y <= x:
                at_or_below += 1
        if at_or_below >= need and (best is None or x < best):
            best = x
    assert best is not None
    return best


def cover_bps(losses_cents: list[int], margin_cents: int) -> int:
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if any(x < 0 for x in losses_cents):
        raise ValueError("losses cannot be negative")
    covered = 0
    for x in losses_cents:
        if x <= margin_cents:
            covered += 1
    return (10_000 * covered) // len(losses_cents)
