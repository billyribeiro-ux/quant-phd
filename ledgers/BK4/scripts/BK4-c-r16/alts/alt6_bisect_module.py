"""Alternative correct implementation 6 (round 16 verifier): bisect on the sorted losses; the layers are a
min-chain written as a loop over a tuple of (name, limit) pairs; the leftover goes by a while loop."""

from __future__ import annotations

import bisect
from dataclasses import dataclass


@dataclass(frozen=True)
class Waterfall:
    """The result of one default, in cents: the three layers, the survivors' payments and the uncovered loss."""

    margin_cents: int
    default_fund_cents: int
    ccp_capital_cents: int
    survivor_cents: dict[int, int]
    uncovered_cents: int


def _refuse_negative(name: str, value: int) -> None:
    if value < 0:
        raise ValueError(f"{name} is negative: {value}")


def waterfall(
    loss_cents: int,
    defaulter_id: int,
    initial_margin_cents: dict[int, int],
    default_fund_cents: dict[int, int],
    ccp_capital_cents: int,
) -> Waterfall:
    _refuse_negative("loss_cents", loss_cents)
    for member in initial_margin_cents:
        _refuse_negative(f"initial_margin_cents[{member}]", initial_margin_cents[member])
    for member in default_fund_cents:
        _refuse_negative(f"default_fund_cents[{member}]", default_fund_cents[member])
    _refuse_negative("ccp_capital_cents", ccp_capital_cents)
    if defaulter_id not in default_fund_cents:
        raise ValueError(f"defaulter_id {defaulter_id} is not a member")
    if defaulter_id not in initial_margin_cents:
        raise ValueError(f"defaulter_id {defaulter_id} has no initial margin entry")

    paid: list[int] = []
    left = loss_cents
    for limit in (initial_margin_cents[defaulter_id], default_fund_cents[defaulter_id], ccp_capital_cents):
        take = min(left, limit)
        paid.append(take)
        left -= take
    residual = left

    survivors = sorted(m for m in default_fund_cents if m != defaulter_id)
    pool = 0
    for m in survivors:
        pool += default_fund_cents[m]
    payments: dict[int, int] = {}
    uncovered = 0
    if residual >= pool:
        payments = {m: default_fund_cents[m] for m in survivors}
        uncovered = residual - pool
    else:
        for m in survivors:
            payments[m] = residual * default_fund_cents[m] // pool
        owed = residual - sum(payments.values())
        index = 0
        while owed > 0:
            m = survivors[index]
            if default_fund_cents[m] > 0:
                payments[m] += 1
                owed -= 1
            index += 1
    return Waterfall(paid[0], paid[1], paid[2], payments, uncovered)


def margin_for_cover(losses_cents: list[int], target_bps: int) -> int:
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if not 1 <= target_bps <= 10_000:
        raise ValueError(f"target_bps must be between 1 and 10000, got {target_bps}")
    if min(losses_cents) < 0:
        raise ValueError("losses cannot be negative")
    ordered = sorted(losses_cents)
    count = len(ordered)
    k = -((-target_bps * count) // 10_000)
    # bisect_right on the k-th value: the smallest loss x with at least k losses at or below x
    return ordered[bisect.bisect_left(ordered, ordered[k - 1])]


def cover_bps(losses_cents: list[int], margin_cents: int) -> int:
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if min(losses_cents) < 0:
        raise ValueError("losses cannot be negative")
    ordered = sorted(losses_cents)
    covered = bisect.bisect_right(ordered, margin_cents)
    return covered * 10_000 // len(ordered)
