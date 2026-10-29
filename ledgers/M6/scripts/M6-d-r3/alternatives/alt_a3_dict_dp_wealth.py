"""Alternative correct engine A3: dictionary dynamic program over wealth states for doubling, memoised recursion elsewhere."""

from __future__ import annotations

import math
from fractions import Fraction
from functools import lru_cache
from typing import Any


def stopped_value_expectation(instance: dict[str, Any]) -> Fraction:
    n = int(instance["horizon"])
    if n < 1:
        raise ValueError("horizon")
    level = int(instance["stop_level"])
    cap = int(instance["stop_cap"])
    if cap > n:
        raise ValueError("cap")
    p = Fraction(instance["win_probability"])

    @lru_cache(maxsize=None)
    def value(pos: int, k: int) -> Fraction:
        # expected S_tau from position pos after k steps (k < cap), with tau = first time == level, or cap
        if k == cap:
            return Fraction(pos)
        return p * step(pos + 1, k + 1) + (1 - p) * step(pos - 1, k + 1)

    def step(pos: int, k: int) -> Fraction:
        if pos == level:
            return Fraction(pos)
        return value(pos, k)

    return step(0, 0) if level != 0 else Fraction(0) * 0 + _stopped_from_start(level, cap, p)


def _stopped_from_start(level: int, cap: int, p: Fraction) -> Fraction:
    # level 0 is first tested after the first step, as the page's convention states
    @lru_cache(maxsize=None)
    def f(pos: int, k: int) -> Fraction:
        if k == cap:
            return Fraction(pos)
        total = Fraction(0)
        for q, nxt in ((p, pos + 1), (1 - p, pos - 1)):
            if nxt == level:
                total += q * nxt
            else:
                total += q * f(nxt, k + 1)
        return total

    return f(0, 0)


def doob_max_probability(instance: dict[str, Any], lam: int) -> tuple[Fraction, Fraction]:
    n = int(instance["horizon"])
    if n < 1:
        raise ValueError("horizon")
    if lam <= 0:
        raise ValueError("lambda")
    half = Fraction(1, 2)
    layer: dict[tuple[int, int], Fraction] = {(0, 0): Fraction(1)}
    for _ in range(n):
        nxt: dict[tuple[int, int], Fraction] = {}
        for (x, m), w in layer.items():
            for y in (x + 1, x - 1):
                key = (y, max(m, abs(y)))
                nxt[key] = nxt.get(key, Fraction(0)) + w * half
        layer = nxt
    prob = sum((w for (_, m), w in layer.items() if m >= lam), Fraction(0))
    bound = sum((abs(x) * w for (x, _), w in layer.items()), Fraction(0)) / lam
    return prob, bound


def doubling_outcome(instance: dict[str, Any]) -> dict[str, int | Fraction]:
    capital = int(instance["capital_cents"])
    base = int(instance["base_stake_cents"])
    if capital <= 0:
        raise ValueError("capital")
    if base > capital:
        raise ValueError("stake")
    p = Fraction(instance["win_probability"])
    # state: wealth before the next bet, with the bet index k; dictionary of wealth -> probability
    states: dict[tuple[int, int], Fraction] = {(capital, 1): Fraction(1)}
    win = Fraction(0)
    ruin = Fraction(0)
    expected = Fraction(0)
    ruin_wealth = None
    bets = None
    while states:
        nxt: dict[tuple[int, int], Fraction] = {}
        for (wealth, k), w in states.items():
            stake = base * 2 ** (k - 1)
            if stake > wealth:
                ruin += w
                expected += w * wealth
                ruin_wealth = wealth
                bets = k - 1
                continue
            win += w * p
            expected += w * p * (wealth + stake)
            nxt[(wealth - stake, k + 1)] = nxt.get((wealth - stake, k + 1), Fraction(0)) + w * (1 - p)
        states = nxt
    assert bets is not None and ruin_wealth is not None
    return {
        "bets_allowed": bets,
        "win_probability": win,
        "ruin_probability": ruin,
        "wealth_on_win_cents": capital + base,
        "wealth_on_ruin_cents": ruin_wealth,
        "max_stake_cents": base * 2 ** (bets - 1),
        "expected_final_wealth_cents": math.floor(expected + Fraction(1, 2)),
    }


def dyadic_martingale_error(instance: dict[str, Any], n: int) -> Fraction:
    # exact sum over cells of the cell integral (x - mid)^2, using the antiderivative (x - mid)^3 / 3
    cells = 2**n
    total = Fraction(0)
    for j in range(cells):
        lo, hi = Fraction(j, cells), Fraction(j + 1, cells)
        mid = (lo + hi) / 2
        total += ((hi - mid) ** 3 - (lo - mid) ** 3) / 3
    return total


def dyadic_martingale_value(instance: dict[str, Any], n: int, x: Fraction) -> Fraction:
    cells = 2**n
    x = Fraction(x)
    if not 0 <= x <= 1:
        raise ValueError("x in [0, 1]")
    j = min(math.floor(x * cells), cells - 1)
    return Fraction(2 * j + 1, 2 * cells)
