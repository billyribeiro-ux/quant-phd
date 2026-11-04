"""Alternative correct implementation 1: comprehensions and sorted(), with a list of positive-fund recipients for the leftover."""

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
    """Layers in order; survivors pro rata with the leftover to the first positive funds in id order."""
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
    margin_paid = min(loss_cents, initial_margin_cents[defaulter_id])
    fund_paid = min(loss_cents - margin_paid, default_fund_cents[defaulter_id])
    capital_paid = min(loss_cents - margin_paid - fund_paid, ccp_capital_cents)
    residual = loss_cents - margin_paid - fund_paid - capital_paid
    survivors = sorted(m for m in default_fund_cents if m != defaulter_id)
    pool = sum(default_fund_cents[m] for m in survivors)
    if residual >= pool:
        shares = {m: default_fund_cents[m] for m in survivors}
        uncovered = residual - pool
    else:
        base = {m: residual * default_fund_cents[m] // pool for m in survivors}
        left = residual - sum(base.values())
        recipients = [m for m in survivors if default_fund_cents[m] > 0][:left]
        shares = {m: base[m] + (1 if m in recipients else 0) for m in survivors}
        uncovered = 0
    return Waterfall(margin_paid, fund_paid, capital_paid, shares, uncovered)


def margin_for_cover(losses_cents: list[int], target_bps: int) -> int:
    """The k-th smallest loss, with k = ceiling of target_bps * S / 10000 written as (x + 9999) // 10000."""
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if not 1 <= target_bps <= 10_000:
        raise ValueError(f"target_bps must be in the range 1 to 10000, not {target_bps}")
    if any(loss < 0 for loss in losses_cents):
        raise ValueError("losses cannot be negative")
    k = (target_bps * len(losses_cents) + 9_999) // 10_000
    return sorted(losses_cents)[k - 1]


def cover_bps(losses_cents: list[int], margin_cents: int) -> int:
    """Floored basis points of scenarios with loss at most the margin."""
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if any(loss < 0 for loss in losses_cents):
        raise ValueError("losses cannot be negative")
    return 10_000 * len([loss for loss in losses_cents if loss <= margin_cents]) // len(losses_cents)
