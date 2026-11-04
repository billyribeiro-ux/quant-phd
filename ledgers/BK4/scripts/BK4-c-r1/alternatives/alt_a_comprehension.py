"""Alternative A (verifier-written, BK4-c): comprehensions and sorted() for sizing, a generator for the waterfall."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Waterfall:
    margin_cents: int
    default_fund_cents: int
    ccp_capital_cents: int
    survivor_cents: dict[int, int]
    uncovered_cents: int


def _validate_amounts(
    loss_cents: int,
    defaulter_id: int,
    initial_margin_cents: dict[int, int],
    default_fund_cents: dict[int, int],
    ccp_capital_cents: int,
) -> None:
    if loss_cents < 0:
        raise ValueError(f"loss_cents is negative: {loss_cents}")
    if any(v < 0 for v in initial_margin_cents.values()):
        raise ValueError("initial_margin_cents holds a negative amount")
    if any(v < 0 for v in default_fund_cents.values()):
        raise ValueError("default_fund_cents holds a negative amount")
    if ccp_capital_cents < 0:
        raise ValueError(f"ccp_capital_cents is negative: {ccp_capital_cents}")
    if defaulter_id not in default_fund_cents or defaulter_id not in initial_margin_cents:
        raise ValueError(f"defaulter_id {defaulter_id} is not one of the member ids")


def _losses_ok(losses_cents: list[int]) -> None:
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if any(x < 0 for x in losses_cents):
        raise ValueError("losses cannot be negative")


def _pay(
    loss: int,
    defaulter_id: int,
    margins: dict[int, int],
    funds: dict[int, int],
    capital: int,
) -> tuple[int, int, int, int]:
    margin_paid = min(loss, margins[defaulter_id])
    fund_paid = min(loss - margin_paid, funds[defaulter_id])
    capital_paid = min(loss - margin_paid - fund_paid, capital)
    return margin_paid, fund_paid, capital_paid, loss - margin_paid - fund_paid - capital_paid


def waterfall(
    loss_cents: int,
    defaulter_id: int,
    initial_margin_cents: dict[int, int],
    default_fund_cents: dict[int, int],
    ccp_capital_cents: int,
) -> Waterfall:
    _validate_amounts(loss_cents, defaulter_id, initial_margin_cents, default_fund_cents, ccp_capital_cents)
    m, f, c, residual = _pay(loss_cents, defaulter_id, initial_margin_cents, default_fund_cents, ccp_capital_cents)
    survivors = sorted(i for i in default_fund_cents if i != defaulter_id)
    pool = sum(default_fund_cents[i] for i in survivors)
    if residual >= pool:
        return Waterfall(m, f, c, {i: default_fund_cents[i] for i in survivors}, residual - pool)
    shares = {i: residual * default_fund_cents[i] // pool for i in survivors}
    extra = residual - sum(shares.values())
    payers = (i for i in survivors if default_fund_cents[i] > 0)
    for i in payers:
        if extra == 0:
            break
        shares[i] += 1
        extra -= 1
    return Waterfall(m, f, c, shares, 0)


def margin_for_cover(losses_cents: list[int], target_bps: int) -> int:
    _losses_ok(losses_cents)
    if not 1 <= target_bps <= 10_000:
        raise ValueError(f"target_bps must lie between 1 and 10000, got {target_bps}")
    n = len(losses_cents)
    k = -((-target_bps * n) // 10_000)
    ordered = sorted([x for x in losses_cents])
    return [v for v in ordered][k - 1]


def cover_bps(losses_cents: list[int], margin_cents: int) -> int:
    _losses_ok(losses_cents)
    covered = len([x for x in losses_cents if x <= margin_cents])
    return 10_000 * covered // len(losses_cents)
