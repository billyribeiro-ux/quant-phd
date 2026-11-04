"""Alternative G (verifier-written, BK4-c round 2): layers as a loop over (cap) pairs, bisect on the sorted losses."""

from __future__ import annotations

import bisect
from dataclasses import dataclass


@dataclass(frozen=True)
class Waterfall:
    margin_cents: int
    default_fund_cents: int
    ccp_capital_cents: int
    survivor_cents: dict[int, int]
    uncovered_cents: int


def waterfall(loss_cents, defaulter_id, initial_margin_cents, default_fund_cents, ccp_capital_cents):  # type: ignore[no-untyped-def]
    if loss_cents < 0:
        raise ValueError(f"the loss_cents input is negative: {loss_cents}")
    if any(v < 0 for v in initial_margin_cents.values()):
        raise ValueError("initial_margin_cents has a negative amount")
    if any(v < 0 for v in default_fund_cents.values()):
        raise ValueError("default_fund_cents has a negative amount")
    if ccp_capital_cents < 0:
        raise ValueError("ccp_capital_cents is negative")
    if defaulter_id not in initial_margin_cents or defaulter_id not in default_fund_cents:
        raise ValueError("defaulter_id is not a member")
    remaining = loss_cents
    paid = []
    for cap in (initial_margin_cents[defaulter_id], default_fund_cents[defaulter_id], ccp_capital_cents):
        take = min(remaining, cap)
        paid.append(take)
        remaining -= take
    residual = remaining
    ids = sorted(m for m in default_fund_cents if m != defaulter_id)
    funds = [default_fund_cents[m] for m in ids]
    total = sum(funds)
    if residual >= total:
        shares = list(funds)
        uncovered = residual - total
    else:
        shares = [residual * f // total for f in funds]
        extra = residual - sum(shares)
        for i, f in enumerate(funds):
            if extra and f > 0:
                shares[i] += 1
                extra -= 1
        uncovered = 0
    return Waterfall(paid[0], paid[1], paid[2], dict(zip(ids, shares)), uncovered)


def margin_for_cover(losses_cents, target_bps):  # type: ignore[no-untyped-def]
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if not (1 <= target_bps <= 10000):
        raise ValueError("target_bps is outside 1 to 10000")
    if min(losses_cents) < 0:
        raise ValueError("losses cannot be negative")
    ordered = sorted(losses_cents)
    s = len(ordered)
    k = (target_bps * s + 9999) // 10000
    return ordered[bisect.bisect_left(range(s), k - 1)]


def cover_bps(losses_cents, margin_cents):  # type: ignore[no-untyped-def]
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if min(losses_cents) < 0:
        raise ValueError("losses cannot be negative")
    ordered = sorted(losses_cents)
    covered = bisect.bisect_right(ordered, margin_cents)
    return 10000 * covered // len(ordered)
