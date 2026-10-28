"""Alternative 2: dictionary dynamic programmes over the walk's (position, peak) states and the doubling wealth."""

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
    mass: dict[int, Fraction] = {0: Fraction(1)}
    total = Fraction(0)
    for _ in range(cap):
        after: dict[int, Fraction] = {}
        for position, weight in mass.items():
            for step, prob in ((1, p), (-1, 1 - p)):
                nxt = position + step
                if nxt == level:
                    total += weight * prob * nxt
                else:
                    after[nxt] = after.get(nxt, Fraction(0)) + weight * prob
        mass = after
    return total + sum((w * pos for pos, w in mass.items()), Fraction(0))


def doob_max_probability(instance: dict[str, Any], lam: int) -> tuple[Fraction, Fraction]:
    horizon = int(instance["horizon"])
    if horizon < 1:
        raise ValueError("the horizon N must be at least 1 step")
    if lam <= 0:
        raise ValueError("the level lambda in Doob's inequality must be a positive number of steps")
    mass: dict[tuple[int, int], Fraction] = {(0, 0): Fraction(1)}
    for _ in range(horizon):
        after: dict[tuple[int, int], Fraction] = {}
        for (position, peak), weight in mass.items():
            for step in (1, -1):
                key = (position + step, max(peak, abs(position + step)))
                after[key] = after.get(key, Fraction(0)) + weight / 2
        mass = after
    hit = sum((w for (_, peak), w in mass.items() if peak >= lam), Fraction(0))
    mean_abs = sum((abs(pos) * w for (pos, _), w in mass.items()), Fraction(0))
    return hit, mean_abs / lam


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
    alive: dict[int, Fraction] = {capital: Fraction(1)}
    win_mass = Fraction(0)
    win_value = Fraction(0)
    ruin_mass = Fraction(0)
    ruin_value = Fraction(0)
    bets = 0
    for bet in range(1, 200):
        stake = base * 2 ** (bet - 1)
        after: dict[int, Fraction] = {}
        for wealth, weight in alive.items():
            if stake > wealth:
                ruin_mass += weight
                ruin_value += weight * wealth
                continue
            win_mass += weight * p
            win_value += weight * p * (wealth + stake)
            after[wealth - stake] = after.get(wealth - stake, Fraction(0)) + weight * (1 - p)
        if not after:
            bets = bet - 1
            break
        alive = after
    expected = win_value + ruin_value
    return {
        "bets_allowed": bets,
        "win_probability": win_mass,
        "ruin_probability": ruin_mass,
        "wealth_on_win_cents": capital + base,
        "wealth_on_ruin_cents": capital - base * (2**bets - 1),
        "max_stake_cents": base * 2 ** (bets - 1),
        "expected_final_wealth_cents": math.floor(expected + Fraction(1, 2)),
    }


def dyadic_martingale_error(instance: dict[str, Any], n: int) -> Fraction:
    if n < 0:
        raise ValueError("the dyadic level n must be a whole number of at least 0")
    cells = 2**n
    width = Fraction(1, cells)
    total = Fraction(0)
    for _ in range(cells):
        total += (width / 2) ** 3 * 2 / 3  # the integral of (x - midpoint)^2 over one cell of width h is h^3 / 12
    return total


def dyadic_martingale_value(instance: dict[str, Any], n: int, x: Fraction) -> Fraction:
    if n < 0:
        raise ValueError("the dyadic level n must be a whole number of at least 0")
    point = Fraction(x)
    if not 0 <= point <= 1:
        raise ValueError("the point x must lie in [0, 1]")
    cells = 2**n
    index = min(int(point * cells), cells - 1)
    return (Fraction(index) + Fraction(1, 2)) / cells
