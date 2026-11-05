"""Round-11 verifier alternative 6: sizing by scanning the distinct losses with an integer cover test (no index formula).

A correct implementation of the page's rules, written by the round-11 verifier in a different style from alt1..alt5.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Waterfall:
    margin_cents: int
    default_fund_cents: int
    ccp_capital_cents: int
    survivor_cents: dict[int, int]
    uncovered_cents: int


def _check_losses(losses_cents: list[int]) -> None:
    if len(losses_cents) == 0:
        raise ValueError("at least one scenario is needed")
    for loss in losses_cents:
        if loss < 0:
            raise ValueError("losses cannot be negative")


def waterfall(
    loss_cents: int,
    defaulter_id: int,
    initial_margin_cents: dict[int, int],
    default_fund_cents: dict[int, int],
    ccp_capital_cents: int,
) -> Waterfall:
    if defaulter_id not in default_fund_cents:
        raise ValueError(f"defaulter_id {defaulter_id} is not one of the member ids")
    if defaulter_id not in initial_margin_cents:
        raise ValueError(f"defaulter_id {defaulter_id} is not one of the member ids")
    for name, value in (("loss_cents", loss_cents), ("ccp_capital_cents", ccp_capital_cents)):
        if value < 0:
            raise ValueError(f"{name} is negative: {value}")
    for member, value in initial_margin_cents.items():
        if value < 0:
            raise ValueError(f"initial_margin_cents is negative for member {member}")
    for member, value in default_fund_cents.items():
        if value < 0:
            raise ValueError(f"default_fund_cents is negative for member {member}")
    layers: list[int] = []
    left = loss_cents
    for cap in (initial_margin_cents[defaulter_id], default_fund_cents[defaulter_id], ccp_capital_cents):
        paid = min(left, cap)
        layers.append(paid)
        left -= paid
    survivors = sorted((m for m in default_fund_cents if m != defaulter_id), reverse=True)[::-1]
    pool = sum(default_fund_cents[m] for m in survivors)
    if left >= pool:
        shares = {m: default_fund_cents[m] for m in survivors}
        uncovered = left - pool
    else:
        shares = {m: left * default_fund_cents[m] // pool for m in survivors}
        spare = left - sum(shares.values())
        for m in survivors:
            if spare and default_fund_cents[m]:
                shares[m] += 1
                spare -= 1
        uncovered = 0
    return Waterfall(layers[0], layers[1], layers[2], shares, uncovered)


def margin_for_cover(losses_cents: list[int], target_bps: int) -> int:
    _check_losses(losses_cents)
    if not 1 <= target_bps <= 10_000:
        raise ValueError(f"target_bps must be between 1 and 10000, got {target_bps}")
    n = len(losses_cents)
    for candidate in sorted(set(losses_cents)):
        if 10_000 * sum(1 for x in losses_cents if x <= candidate) >= target_bps * n:
            return candidate
    raise AssertionError("unreachable: the largest loss covers every scenario")


def cover_bps(losses_cents: list[int], margin_cents: int) -> int:
    _check_losses(losses_cents)
    hits = sum(map(lambda x: 1 if x <= margin_cents else 0, losses_cents))
    return (hits * 10_000) // len(losses_cents)
