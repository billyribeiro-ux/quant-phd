"""Verifier alternative 1: doubling by a sum over the bet at which the first win occurs; the other functions by path recursion."""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any


def _check_horizon(instance: dict[str, Any]) -> int:
    horizon = int(instance["horizon"])
    if horizon < 1:
        raise ValueError("the horizon N must be at least 1 step")
    return horizon


def stopped_value_expectation(instance: dict[str, Any]) -> Fraction:
    horizon = _check_horizon(instance)
    level = int(instance["stop_level"])
    cap = int(instance["stop_cap"])
    if cap > horizon:
        raise ValueError("the stopping rule is not bounded by the horizon N: its cap is above N")
    p = Fraction(instance["win_probability"])
    q = 1 - p

    def walk(position: int, steps_left: int, weight: Fraction, taken: int) -> Fraction:
        if position == level or steps_left == 0:
            return weight * position
        return walk(position + 1, steps_left - 1, weight * p, taken + 1) + walk(
            position - 1, steps_left - 1, weight * q, taken + 1
        )

    return walk(0, cap, Fraction(1), 0)


def doob_max_probability(instance: dict[str, Any], lam: int) -> tuple[Fraction, Fraction]:
    horizon = _check_horizon(instance)
    if lam <= 0:
        raise ValueError("the level lambda in Doob's inequality must be a positive number of steps")
    hits = Fraction(0)
    mean_abs = Fraction(0)
    half = Fraction(1, 2)

    def walk(position: int, peak: int, steps_left: int, weight: Fraction) -> None:
        nonlocal hits, mean_abs
        if steps_left == 0:
            if peak >= lam:
                hits += weight
            mean_abs += weight * abs(position)
            return
        for step in (1, -1):
            walk(position + step, max(peak, abs(position + step)), steps_left - 1, weight * half)

    walk(0, 0, horizon, Fraction(1))
    return hits, mean_abs / lam


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
    # The bets placed: bet k is placed when its stake fits the wealth after k - 1 losses.
    placed = 0
    wealth = capital
    while base * 2**placed <= wealth:
        wealth -= base * 2**placed
        placed += 1
    # Sum over the bet at which the first win occurs, plus the ruin branch after all placed bets lose.
    win = Fraction(0)
    expected = Fraction(0)
    weight = Fraction(1)
    for k in range(1, placed + 1):
        branch = weight * p
        win += branch
        expected += branch * (capital + base)
        weight *= 1 - p
    ruin = weight
    wealth_on_ruin = capital - base * (2**placed - 1)
    expected += ruin * wealth_on_ruin
    cents = math.floor(expected + Fraction(1, 2))
    return {
        "bets_allowed": placed,
        "win_probability": win,
        "ruin_probability": ruin,
        "wealth_on_win_cents": capital + base,
        "wealth_on_ruin_cents": wealth_on_ruin,
        "max_stake_cents": base * 2 ** (placed - 1),
        "expected_final_wealth_cents": cents,
    }


def dyadic_martingale_error(instance: dict[str, Any], n: int) -> Fraction:
    if n < 0:
        raise ValueError("the dyadic level n must be a whole number of at least 0")
    cells = 2**n
    h = Fraction(1, cells)
    per_cell = h**3 / 12  # integral of (x - midpoint)^2 over a cell of width h
    return cells * per_cell


def dyadic_martingale_value(instance: dict[str, Any], n: int, x: Fraction) -> Fraction:
    if n < 0:
        raise ValueError("the dyadic level n must be a whole number of at least 0")
    point = Fraction(x)
    if not 0 <= point <= 1:
        raise ValueError("the point x must lie in [0, 1]")
    cells = 2**n
    j = min(math.floor(point * cells), cells - 1)
    return (Fraction(j) + Fraction(1, 2)) / cells
