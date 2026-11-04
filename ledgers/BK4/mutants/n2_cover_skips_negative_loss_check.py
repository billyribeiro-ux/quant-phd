"""Student error: cover_bps does not refuse a negative loss; only margin_for_cover checks the sign of the losses."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Waterfall:
    """The result of one default: the three layers, the survivors' payments and the uncovered loss, all in cents."""

    margin_cents: int
    default_fund_cents: int
    ccp_capital_cents: int
    survivor_cents: dict[int, int]
    uncovered_cents: int


def _no_negative_losses(losses_cents: list[int]) -> None:
    if any(loss < 0 for loss in losses_cents):
        raise ValueError("losses cannot be negative")


def waterfall(
    loss_cents: int,
    defaulter_id: int,
    initial_margin_cents: dict[int, int],
    default_fund_cents: dict[int, int],
    ccp_capital_cents: int,
) -> Waterfall:
    """Pay one loss through the CCP default waterfall and return the layers and the survivors' payments."""
    if loss_cents < 0:
        raise ValueError(f"loss_cents is negative, and a loss cannot be negative: {loss_cents}")
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

    survivors = sorted(member for member in default_fund_cents if member != defaulter_id)
    total_fund = sum(default_fund_cents[member] for member in survivors)
    survivor_cents: dict[int, int] = {}
    uncovered = 0
    if residual >= total_fund:
        for member in survivors:
            survivor_cents[member] = default_fund_cents[member]
        uncovered = residual - total_fund
    else:
        # total_fund > residual >= 0 here, so the division is safe.
        for member in survivors:
            survivor_cents[member] = residual * default_fund_cents[member] // total_fund
        leftover = residual - sum(survivor_cents.values())
        for member in survivors:
            if leftover == 0:
                break
            if default_fund_cents[member] > 0:
                survivor_cents[member] += 1
                leftover -= 1

    return Waterfall(
        margin_cents=margin_paid,
        default_fund_cents=fund_paid,
        ccp_capital_cents=capital_paid,
        survivor_cents=survivor_cents,
        uncovered_cents=uncovered,
    )


def margin_for_cover(losses_cents: list[int], target_bps: int) -> int:
    """The least margin whose cover is at least target_bps: the k-th smallest loss, k = ceil(target_bps * S / 10000)."""
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if not 1 <= target_bps <= 10_000:
        raise ValueError(f"target_bps must be in the range 1 to 10000, not {target_bps}")
    _no_negative_losses(losses_cents)
    count = len(losses_cents)
    index = -((-target_bps * count) // 10_000)
    return sorted(losses_cents)[index - 1]


def cover_bps(losses_cents: list[int], margin_cents: int) -> int:
    """The share of scenarios whose loss the margin covers in full, in basis points, floored."""
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    covered = sum(1 for loss in losses_cents if loss <= margin_cents)
    return 10_000 * covered // len(losses_cents)
