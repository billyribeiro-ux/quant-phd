"""Alternative correct implementation 2: a ClearingHouse class whose methods return the frozen Waterfall."""

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


class ClearingHouse:
    """A clearing house with fixed member margins, default funds and capital, all in integer cents."""

    def __init__(self, initial_margin_cents: dict[int, int], default_fund_cents: dict[int, int], capital: int) -> None:
        self._margins = dict(initial_margin_cents)
        self._funds = dict(default_fund_cents)
        self._capital = capital

    def pay(self, loss: int, defaulter: int) -> Waterfall:
        """Pay one default: margin, then default fund, then capital, then the survivors pro rata."""
        if loss < 0:
            raise ValueError(f"loss_cents is negative: {loss}")
        if any(v < 0 for v in self._margins.values()):
            raise ValueError("initial_margin_cents is negative for some member")
        if any(v < 0 for v in self._funds.values()):
            raise ValueError("default_fund_cents is negative for some member")
        if self._capital < 0:
            raise ValueError(f"ccp_capital_cents is negative: {self._capital}")
        if defaulter not in self._funds or defaulter not in self._margins:
            raise ValueError(f"defaulter_id {defaulter} is not one of the member ids")
        a1 = min(loss, self._margins[defaulter])
        a2 = min(loss - a1, self._funds[defaulter])
        a3 = min(loss - a1 - a2, self._capital)
        r = loss - a1 - a2 - a3
        others = sorted(self._funds.keys() - {defaulter})
        total = sum(self._funds[m] for m in others)
        if r >= total:
            return Waterfall(a1, a2, a3, {m: self._funds[m] for m in others}, r - total)
        pay = {m: (r * self._funds[m]) // total for m in others}
        left = r - sum(pay.values())
        for m in others:
            if left and self._funds[m] > 0:
                pay[m] += 1
                left -= 1
        return Waterfall(a1, a2, a3, pay, 0)


def waterfall(
    loss_cents: int,
    defaulter_id: int,
    initial_margin_cents: dict[int, int],
    default_fund_cents: dict[int, int],
    ccp_capital_cents: int,
) -> Waterfall:
    """Module function: delegates to ClearingHouse.pay, after the validation the page names."""
    if loss_cents < 0:
        raise ValueError(f"loss_cents is negative, and a loss cannot be negative: {loss_cents}")
    return ClearingHouse(initial_margin_cents, default_fund_cents, ccp_capital_cents).pay(loss_cents, defaulter_id)


def margin_for_cover(losses_cents: list[int], target_bps: int) -> int:
    """Module function: the k-th smallest loss with k from the ceiling, in the class's style of exact integers."""
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if not 1 <= target_bps <= 10_000:
        raise ValueError(f"target_bps must be in the range 1 to 10000, not {target_bps}")
    if any(loss < 0 for loss in losses_cents):
        raise ValueError("losses cannot be negative")
    k = -((-target_bps * len(losses_cents)) // 10_000)
    return sorted(losses_cents)[k - 1]


def cover_bps(losses_cents: list[int], margin_cents: int) -> int:
    """Module function: floored basis points covered by the margin."""
    if not losses_cents:
        raise ValueError("at least one scenario is needed")
    if any(loss < 0 for loss in losses_cents):
        raise ValueError("losses cannot be negative")
    covered = sum(1 for loss in losses_cents if loss <= margin_cents)
    return (10_000 * covered) // len(losses_cents)
