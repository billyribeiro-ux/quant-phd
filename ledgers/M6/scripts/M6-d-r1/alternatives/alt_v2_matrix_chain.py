"""Verifier alternative 2: the doubling chain as a transition matrix over (wealth state, bet index) with exact Fractions."""

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
    # Vector over positions -(cap) .. cap of the mass still running; absorbed mass is accumulated in total.
    width = cap
    mass = {x: Fraction(0) for x in range(-width, width + 1)}
    mass[0] = Fraction(1)
    total = Fraction(0)
    for _ in range(cap):
        nxt = {x: Fraction(0) for x in mass}
        for x, m in mass.items():
            if m == 0:
                continue
            for step, pr in ((1, p), (-1, 1 - p)):
                y = x + step
                if y == level:
                    total += m * pr * y
                else:
                    nxt[y] += m * pr
        mass = nxt
    total += sum((m * x for x, m in mass.items()), Fraction(0))
    return total


def doob_max_probability(instance: dict[str, Any], lam: int) -> tuple[Fraction, Fraction]:
    horizon = int(instance["horizon"])
    if horizon < 1:
        raise ValueError("the horizon N must be at least 1 step")
    if lam <= 0:
        raise ValueError("the level lambda in Doob's inequality must be a positive number of steps")
    # Two-component states: (position, already reached lam).
    state = {(0, False): Fraction(1)}
    for _ in range(horizon):
        nxt: dict[tuple[int, bool], Fraction] = {}
        for (x, r), m in state.items():
            for step in (1, -1):
                y = x + step
                key = (y, r or abs(y) >= lam)
                nxt[key] = nxt.get(key, Fraction(0)) + m / 2
        state = nxt
    prob = sum((m for (_, r), m in state.items() if r), Fraction(0))
    mean_abs = sum((abs(x) * m for (x, _), m in state.items()), Fraction(0))
    return prob, mean_abs / lam


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
    # States: wealth on hand before the next bet; bet index implied by the wealth. Each state either wins or loses.
    alive: dict[int, Fraction] = {capital: Fraction(1)}
    win = Fraction(0)
    expected = Fraction(0)
    bets_placed = 0
    bet_index = 1
    while alive:
        nxt: dict[int, Fraction] = {}
        stake = base * 2 ** (bet_index - 1)
        for wealth, m in alive.items():
            if stake <= wealth:
                win += m * p
                expected += m * p * (wealth + stake)
                nxt[wealth - stake] = nxt.get(wealth - stake, Fraction(0)) + m * (1 - p)
            else:
                expected += m * wealth
                ruin_wealth = wealth
                bets_placed = bet_index - 1
                nxt_ruin = (ruin_wealth, m)
                _ = nxt_ruin
        if any(stake <= w for w in alive):
            bet_index += 1
            alive = {w: m for w, m in nxt.items()}
        else:
            break
    ruin_mass = (1 - p) ** bets_placed
    wealth_on_ruin = capital - base * (2**bets_placed - 1)
    expected = win * (capital + base) + ruin_mass * wealth_on_ruin
    return {
        "bets_allowed": bets_placed,
        "win_probability": 1 - ruin_mass,
        "ruin_probability": ruin_mass,
        "wealth_on_win_cents": capital + base,
        "wealth_on_ruin_cents": wealth_on_ruin,
        "max_stake_cents": base * 2 ** (bets_placed - 1),
        "expected_final_wealth_cents": math.floor(expected + Fraction(1, 2)),
    }


def dyadic_martingale_error(instance: dict[str, Any], n: int) -> Fraction:
    if n < 0:
        raise ValueError("the dyadic level n must be a whole number of at least 0")
    total = Fraction(0)
    cells = 2**n
    for j in range(cells):
        a, b = Fraction(j, cells), Fraction(j + 1, cells)
        c = (a + b) / 2
        # Midpoint-centred second moment over the cell, from the antiderivative of (x - c)^2.
        total += ((b - c) ** 3 - (a - c) ** 3) / 3
    return total


def dyadic_martingale_value(instance: dict[str, Any], n: int, x: Fraction) -> Fraction:
    if n < 0:
        raise ValueError("the dyadic level n must be a whole number of at least 0")
    point = Fraction(x)
    if not 0 <= point <= 1:
        raise ValueError("the point x must lie in [0, 1]")
    cells = 2**n
    for j in range(cells):
        a, b = Fraction(j, cells), Fraction(j + 1, cells)
        if a <= point < b or (j == cells - 1 and point == b):
            return (a + b) / 2
    raise AssertionError("unreachable: every point of [0, 1] lies in a cell")
