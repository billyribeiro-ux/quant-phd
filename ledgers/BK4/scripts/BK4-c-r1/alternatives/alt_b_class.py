"""Alternative B (verifier-written, BK4-c): a class-based ClearingHouse whose methods return the frozen Waterfall."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Waterfall:
    margin_cents: int
    default_fund_cents: int
    ccp_capital_cents: int
    survivor_cents: dict[int, int]
    uncovered_cents: int


class ClearingHouse:
    def __init__(
        self,
        defaulter_id: int,
        initial_margin_cents: dict[int, int],
        default_fund_cents: dict[int, int],
        ccp_capital_cents: int,
    ) -> None:
        for member, amount in initial_margin_cents.items():
            if amount < 0:
                raise ValueError(f"initial_margin_cents is negative for member {member}: {amount}")
        for member, amount in default_fund_cents.items():
            if amount < 0:
                raise ValueError(f"default_fund_cents is negative for member {member}: {amount}")
        if ccp_capital_cents < 0:
            raise ValueError(f"ccp_capital_cents is negative: {ccp_capital_cents}")
        if defaulter_id not in default_fund_cents or defaulter_id not in initial_margin_cents:
            raise ValueError(f"defaulter_id {defaulter_id} is not one of the member ids")
        self._defaulter = defaulter_id
        self._margins = dict(initial_margin_cents)
        self._funds = dict(default_fund_cents)
        self._capital = ccp_capital_cents

    def survivors(self) -> list[int]:
        return sorted(m for m in self._funds if m != self._defaulter)

    def pay(self, loss_cents: int) -> Waterfall:
        if loss_cents < 0:
            raise ValueError(f"loss_cents is negative: {loss_cents}")
        layer_margin = min(loss_cents, self._margins[self._defaulter])
        layer_fund = min(loss_cents - layer_margin, self._funds[self._defaulter])
        layer_capital = min(loss_cents - layer_margin - layer_fund, self._capital)
        residual = loss_cents - layer_margin - layer_fund - layer_capital
        members = self.survivors()
        pool = sum(self._funds[m] for m in members)
        if residual >= pool:
            return Waterfall(layer_margin, layer_fund, layer_capital, {m: self._funds[m] for m in members}, residual - pool)
        pay_out = {m: residual * self._funds[m] // pool for m in members}
        left = residual - sum(pay_out.values())
        for m in members:
            if left > 0 and self._funds[m] > 0:
                pay_out[m] += 1
                left -= 1
        return Waterfall(layer_margin, layer_fund, layer_capital, pay_out, 0)


def waterfall(
    loss_cents: int,
    defaulter_id: int,
    initial_margin_cents: dict[int, int],
    default_fund_cents: dict[int, int],
    ccp_capital_cents: int,
) -> Waterfall:
    house = ClearingHouse(defaulter_id, initial_margin_cents, default_fund_cents, ccp_capital_cents)
    return house.pay(loss_cents)


def margin_for_cover(losses_cents: list[int], target_bps: int) -> int:
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if not 1 <= target_bps <= 10_000:
        raise ValueError(f"target_bps must be within 1 to 10000: {target_bps}")
    if any(x < 0 for x in losses_cents):
        raise ValueError("losses cannot be negative")
    count = len(losses_cents)
    position = -((-target_bps * count) // 10_000)
    ranked = sorted(losses_cents)
    return ranked[position - 1]


def cover_bps(losses_cents: list[int], margin_cents: int) -> int:
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if any(x < 0 for x in losses_cents):
        raise ValueError("losses cannot be negative")
    return 10_000 * sum(1 for x in losses_cents if x <= margin_cents) // len(losses_cents)
