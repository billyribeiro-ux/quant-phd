"""Alternative 3: a transition-matrix formulation of the doubling chain, with path enumeration for the walks."""

from __future__ import annotations

import itertools
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
    total = Fraction(0)
    for steps in itertools.product((1, -1), repeat=horizon):
        prob = Fraction(1)
        for step in steps:
            prob *= p if step == 1 else 1 - p
        hit = None
        position = 0
        for index, step in enumerate(steps[:cap]):
            position += step
            if position == level:
                hit = index
                break
        value = level if hit is not None else sum(steps[:cap])
        total += prob * value
    return total


def doob_max_probability(instance: dict[str, Any], lam: int) -> tuple[Fraction, Fraction]:
    horizon = int(instance["horizon"])
    if horizon < 1:
        raise ValueError("the horizon N must be at least 1 step")
    if lam <= 0:
        raise ValueError("the level lambda in Doob's inequality must be a positive number of steps")
    count = Fraction(0)
    mean_abs = Fraction(0)
    for steps in itertools.product((1, -1), repeat=horizon):
        position = 0
        peak = 0
        for step in steps:
            position += step
            peak = max(peak, abs(position))
        if peak >= lam:
            count += 1
        mean_abs += abs(position)
    total = Fraction(2**horizon)
    return count / total, (mean_abs / total) / lam


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
    # State j = number of bets lost so far. Index len(states) - 1 is the last state that can still place a bet.
    wealth = []
    j = 0
    while base * 2**j <= capital - base * (2**j - 1):
        wealth.append(capital - base * (2**j - 1))
        j += 1
    bets = len(wealth)
    size = bets + 1  # states 0..bets-1 are live, state bets is the ruin state
    matrix = [[Fraction(0)] * size for _ in range(size)]
    for j in range(bets):
        matrix[j][j + 1 if j + 1 < size else j] = 1 - p
    vector = [Fraction(0)] * size
    vector[0] = Fraction(1)
    win = Fraction(0)
    for j in range(bets):
        win += vector[j] * p
        vector = [sum((vector[i] * matrix[i][k] for i in range(size)), Fraction(0)) for k in range(size)]
    ruin = Fraction(1) - win
    expected = win * (capital + base) + ruin * (capital - base * (2**bets - 1))
    return {
        "bets_allowed": bets,
        "win_probability": win,
        "ruin_probability": ruin,
        "wealth_on_win_cents": capital + base,
        "wealth_on_ruin_cents": capital - base * (2**bets - 1),
        "max_stake_cents": base * 2 ** (bets - 1),
        "expected_final_wealth_cents": math.floor(expected + Fraction(1, 2)),
    }


def dyadic_martingale_error(instance: dict[str, Any], n: int) -> Fraction:
    if n < 0:
        raise ValueError("the dyadic level n must be a whole number of at least 0")
    cells = 2**n
    total = Fraction(0)
    for j in range(cells):
        a = Fraction(j, cells)
        b = Fraction(j + 1, cells)
        c = (a + b) / 2
        total += ((b - c) ** 3 - (a - c) ** 3) / 3
    return total


def dyadic_martingale_value(instance: dict[str, Any], n: int, x: Fraction) -> Fraction:
    if n < 0:
        raise ValueError("the dyadic level n must be a whole number of at least 0")
    point = Fraction(x)
    if not 0 <= point <= 1:
        raise ValueError("the point x must lie in [0, 1]")
    cells = 2**n
    index = min(int(point * cells), cells - 1)
    return Fraction(2 * index + 1, 2 * cells)
