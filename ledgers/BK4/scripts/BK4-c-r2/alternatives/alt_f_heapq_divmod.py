"""Alternative F (verifier-written, BK4-c round 2): heapq.nsmallest for sizing, divmod for shares, validation by name."""

from __future__ import annotations

import heapq
from dataclasses import dataclass


@dataclass(frozen=True)
class Waterfall:
    margin_cents: int
    default_fund_cents: int
    ccp_capital_cents: int
    survivor_cents: dict[int, int]
    uncovered_cents: int


def _refuse_negative(name: str, value: int) -> None:
    if value < 0:
        raise ValueError(f"{name} is negative: {value}")


def waterfall(loss_cents, defaulter_id, initial_margin_cents, default_fund_cents, ccp_capital_cents):  # type: ignore[no-untyped-def]
    if defaulter_id not in default_fund_cents:
        raise ValueError(f"defaulter_id {defaulter_id} is not one of the member ids")
    _refuse_negative("loss_cents", loss_cents)
    for member in initial_margin_cents:
        _refuse_negative("initial_margin_cents", initial_margin_cents[member])
    for member in default_fund_cents:
        _refuse_negative("default_fund_cents", default_fund_cents[member])
    _refuse_negative("ccp_capital_cents", ccp_capital_cents)
    im = initial_margin_cents[defaulter_id]
    df = default_fund_cents[defaulter_id]
    a1 = min(loss_cents, im)
    a2 = min(loss_cents - a1, df)
    a3 = min(loss_cents - a1 - a2, ccp_capital_cents)
    residual = loss_cents - a1 - a2 - a3
    members = sorted(m for m in default_fund_cents if m != defaulter_id)
    pool = sum(default_fund_cents[m] for m in members)
    out: dict[int, int] = {}
    uncovered = 0
    if residual >= pool:
        out = {m: default_fund_cents[m] for m in members}
        uncovered = residual - pool
    else:
        for m in members:
            out[m], _ = divmod(residual * default_fund_cents[m], pool)
        left = residual - sum(out.values())
        for m in members:
            if left and default_fund_cents[m] > 0:
                out[m] += 1
                left -= 1
    return Waterfall(a1, a2, a3, out, uncovered)


def margin_for_cover(losses_cents, target_bps):  # type: ignore[no-untyped-def]
    if len(losses_cents) == 0:
        raise ValueError("at least one scenario is needed")
    if target_bps < 1 or target_bps > 10000:
        raise ValueError(f"target_bps must be between 1 and 10000, got {target_bps}")
    if any(x < 0 for x in losses_cents):
        raise ValueError("losses cannot be negative")
    s = len(losses_cents)
    k = -(-(target_bps * s) // 10000)
    return heapq.nsmallest(k, losses_cents)[-1]


def cover_bps(losses_cents, margin_cents):  # type: ignore[no-untyped-def]
    if len(losses_cents) == 0:
        raise ValueError("at least one scenario is needed")
    if any(x < 0 for x in losses_cents):
        raise ValueError("losses cannot be negative")
    return sum(1 for x in losses_cents if x <= margin_cents) * 10000 // len(losses_cents)
