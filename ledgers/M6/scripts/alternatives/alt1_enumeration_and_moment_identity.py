"""Alternative 1: enumeration for the walks, a sum over stopping levels for doubling, and the variance identity for the dyadic error."""

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
        weight = Fraction(1)
        for step in steps:
            weight *= p if step == 1 else 1 - p
        position = 0
        stopped = None
        for step in steps[:cap]:
            position += step
            if position == level:
                stopped = position
                break
        total += weight * (stopped if stopped is not None else sum(steps[:cap]))
    return total


def doob_max_probability(instance: dict[str, Any], lam: int) -> tuple[Fraction, Fraction]:
    horizon = int(instance["horizon"])
    if horizon < 1:
        raise ValueError("the horizon N must be at least 1 step")
    if lam <= 0:
        raise ValueError("the level lambda in Doob's inequality must be a positive number of steps")
    hits = Fraction(0)
    first_moment = Fraction(0)
    weight = Fraction(1, 2**horizon)
    for steps in itertools.product((1, -1), repeat=horizon):
        position = 0
        peak = 0
        for step in steps:
            position += step
            peak = max(peak, abs(position))
        hits += weight if peak >= lam else 0
        first_moment += weight * abs(position)
    return hits, first_moment / lam


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
    bets = ((capital + base) // base).bit_length() - 1  # the largest j with base * 2**j <= capital + base
    q = 1 - p
    win_on_bet = [q**w * p for w in range(bets)]
    win = sum(win_on_bet, Fraction(0))
    ruin = q**bets
    wealth_on_win = capital + base
    wealth_on_ruin = capital - base * (2**bets - 1)
    expected = sum((prob * wealth_on_win for prob in win_on_bet), Fraction(0)) + ruin * wealth_on_ruin
    return {
        "bets_allowed": bets,
        "win_probability": win,
        "ruin_probability": ruin,
        "wealth_on_win_cents": wealth_on_win,
        "wealth_on_ruin_cents": wealth_on_ruin,
        "max_stake_cents": base * 2 ** (bets - 1),
        "expected_final_wealth_cents": math.floor(expected + Fraction(1, 2)),
    }


def dyadic_martingale_error(instance: dict[str, Any], n: int) -> Fraction:
    if n < 0:
        raise ValueError("the dyadic level n must be a whole number of at least 0")
    cells = 2**n
    second_moment_of_m = Fraction(0)
    for j in range(cells):
        midpoint = (Fraction(j) + Fraction(1, 2)) / cells
        second_moment_of_m += midpoint * midpoint / cells
    return Fraction(1, 3) - second_moment_of_m


def dyadic_martingale_value(instance: dict[str, Any], n: int, x: Fraction) -> Fraction:
    if n < 0:
        raise ValueError("the dyadic level n must be a whole number of at least 0")
    point = Fraction(x)
    if not 0 <= point <= 1:
        raise ValueError("the point x must lie in [0, 1]")
    cells = 2**n
    index = min(int(point * cells), cells - 1)
    return (Fraction(index) + Fraction(1, 2)) / cells
