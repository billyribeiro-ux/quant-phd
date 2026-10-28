"""Alternative 4: float evaluation of the doubling cents with the half-up rule, exact Fractions everywhere else."""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any


def stopped_value_expectation(instance: dict[str, Any]) -> Fraction:
    horizon = int(instance["horizon"])
    if horizon < 1:
        raise ValueError("the horizon N must be at least 1 step")
    level = int(instance["stop_level"])
    cap = int(instance["stop_cap"])
    if cap > horizon:
        raise ValueError("the stopping rule is not bounded by the horizon N: its cap is above N")
    p = Fraction(instance["win_probability"])
    dist: dict[tuple[int, int], Fraction] = {(0, 0): Fraction(1)}  # (position, steps taken); stopped paths leave
    total = Fraction(0)
    for _ in range(cap):
        nxt: dict[tuple[int, int], Fraction] = {}
        for (position, taken), weight in dist.items():
            for step, prob in ((1, p), (-1, 1 - p)):
                new = position + step
                if new == level:
                    total += weight * prob * new
                else:
                    key = (new, taken + 1)
                    nxt[key] = nxt.get(key, Fraction(0)) + weight * prob
        dist = nxt
    total += sum((w * pos for (pos, _), w in dist.items()), Fraction(0))
    return total


def doob_max_probability(instance: dict[str, Any], lam: int) -> tuple[Fraction, Fraction]:
    horizon = int(instance["horizon"])
    if horizon < 1:
        raise ValueError("the horizon N must be at least 1 step")
    if lam <= 0:
        raise ValueError("the level lambda in Doob's inequality must be a positive number of steps")
    states: dict[tuple[int, bool], Fraction] = {(0, False): Fraction(1)}
    for _ in range(horizon):
        nxt: dict[tuple[int, bool], Fraction] = {}
        for (pos, seen), w in states.items():
            for step in (1, -1):
                key = (pos + step, seen or abs(pos + step) >= lam)
                nxt[key] = nxt.get(key, Fraction(0)) + w / 2
        states = nxt
    prob = sum((w for (_, seen), w in states.items() if seen), Fraction(0))
    return prob, sum((abs(pos) * w for (pos, _), w in states.items()), Fraction(0)) / lam


def doubling_outcome(instance: dict[str, Any]) -> dict[str, int | Fraction]:
    capital = int(instance["capital_cents"])
    base = int(instance["base_stake_cents"])
    if capital <= 0:
        raise ValueError("the capital must be a positive number of cents")
    if base > capital:
        raise ValueError("a stake larger than the capital is not allowed: the first stake must not exceed capital")
    if base <= 0:
        raise ValueError("the base stake must be a positive number of cents")
    p = Fraction(instance["win_probability"])
    bets = 0
    while base * 2 ** (bets + 1) <= capital + base:
        bets += 1
    q = 1 - p
    ruin = q**bets
    wealth_on_ruin = capital - base * (2**bets - 1)
    # Float evaluation of the expectation, then one half-up rounding of the cents.
    pf = float(p)
    expected_float = (1.0 - (1.0 - pf) ** bets) * (capital + base) + (1.0 - pf) ** bets * wealth_on_ruin
    return {
        "bets_allowed": bets,
        "win_probability": 1 - ruin,
        "ruin_probability": ruin,
        "wealth_on_win_cents": capital + base,
        "wealth_on_ruin_cents": wealth_on_ruin,
        "max_stake_cents": base * 2 ** (bets - 1),
        "expected_final_wealth_cents": math.floor(expected_float + 0.5),
    }


def dyadic_martingale_error(instance: dict[str, Any], n: int) -> Fraction:
    if n < 0:
        raise ValueError("the dyadic level n must be a whole number of at least 0")
    return Fraction(1, 12 * 4**n)


def dyadic_martingale_value(instance: dict[str, Any], n: int, x: Fraction) -> Fraction:
    if n < 0:
        raise ValueError("the dyadic level n must be a whole number of at least 0")
    point = Fraction(x)
    if not 0 <= point <= 1:
        raise ValueError("the point x must lie in [0, 1]")
    cells = 2**n
    index = min(int(point * cells), cells - 1)
    return Fraction(2 * index + 1, 2 * cells)
