"""The stopped walk gives a down step the weight p, not 1 - p, so the weights do not sum to 1 on a biased coin.

Based on the reference solution; the single change is marked in the code.

Every probability is an exact Fraction. Every money amount is an integer number of cents, computed from an exact
Fraction and rounded once, half up.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any


def _horizon(instance: dict[str, Any]) -> int:
    """The horizon N of the instance. The specification requires N >= 1."""
    horizon = int(instance["horizon"])
    if horizon < 1:
        raise ValueError("the horizon N must be at least 1 step")
    return horizon


def _win_probability(instance: dict[str, Any]) -> Fraction:
    """The probability of an up step, as an exact Fraction strictly between 0 and 1."""
    p = Fraction(instance["win_probability"])
    if not 0 < p < 1:
        raise ValueError("the win probability must lie strictly between 0 and 1")
    return p


def _nearest_cent(amount: Fraction) -> int:
    """An exact amount in cents, rounded once, half up: floor(x + 1/2) for a non-negative x."""
    return math.floor(amount + Fraction(1, 2))


def stopped_value_expectation(instance: dict[str, Any]) -> Fraction:
    """E[S_tau] for the walk S from 0 and the stopping rule tau = min(first time S = stop_level, stop_cap).

    The rule is bounded by the horizon N: a cap above N raises ValueError. The answer is exact.
    """
    horizon = _horizon(instance)
    level = int(instance["stop_level"])
    cap = int(instance["stop_cap"])
    if cap > horizon:
        raise ValueError("the stopping rule is not bounded by the horizon N: its cap is above N")
    p = _win_probability(instance)
    alive: dict[int, Fraction] = {0: Fraction(1)}
    total = Fraction(0)
    for _ in range(cap):
        nxt: dict[int, Fraction] = {}
        for position, weight in alive.items():
            for step, prob in ((1, p), (-1, p)):  # MUTANT: the single change

                new_position = position + step
                branch = weight * prob
                if new_position == level:
                    total += branch * new_position
                else:
                    nxt[new_position] = nxt.get(new_position, Fraction(0)) + branch
        alive = nxt
    total += sum((weight * position for position, weight in alive.items()), Fraction(0))
    return total


def doob_max_probability(instance: dict[str, Any], lam: int) -> tuple[Fraction, Fraction]:
    """For the fair walk X_k = |S_k|, k = 0..N: (P(max X_k >= lam), E[X_N] / lam), both exact.

    The first number is the probability on the left of Doob's inequality and the second is its bound.
    """
    horizon = _horizon(instance)
    if lam <= 0:
        raise ValueError("the level lambda in Doob's inequality must be a positive number of steps")
    half = Fraction(1, 2)
    alive: dict[tuple[int, bool], Fraction] = {(0, False): Fraction(1)}
    for _ in range(horizon):
        nxt: dict[tuple[int, bool], Fraction] = {}
        for (position, reached), weight in alive.items():
            for step in (1, -1):
                new_position = position + step
                key = (new_position, reached or abs(new_position) >= lam)
                nxt[key] = nxt.get(key, Fraction(0)) + weight * half
        alive = nxt
    probability = sum((w for (_, reached), w in alive.items() if reached), Fraction(0))
    expected_abs = sum((abs(position) * w for (position, _), w in alive.items()), Fraction(0))
    return probability, expected_abs / lam


def doubling_outcome(instance: dict[str, Any]) -> dict[str, int | Fraction]:
    """The doubling strategy with finite capital: bet k stakes base * 2**(k-1) cents, a win pays the stake.

    A bet is placed only while its stake does not exceed the wealth on hand; the first bet that is not placed, or the
    first win, stops the strategy. Returned keys:
    bets_allowed (J, the number of bets placed when every placed bet loses), win_probability, ruin_probability,
    wealth_on_win_cents, wealth_on_ruin_cents, max_stake_cents, and expected_final_wealth_cents (rounded once, half up).
    """
    capital = int(instance["capital_cents"])
    base = int(instance["base_stake_cents"])
    if capital <= 0:
        raise ValueError("the capital must be a positive number of cents")
    if base > capital:
        raise ValueError("a stake larger than the capital is not allowed: the first stake must not exceed capital")
    if base <= 0:
        raise ValueError("the base stake must be a positive number of cents")
    p = _win_probability(instance)
    bets = 0
    while base * 2 ** (bets + 1) <= capital + base:
        bets += 1
    ruin = (1 - p) ** bets
    win = 1 - ruin
    wealth_on_win = capital + base
    wealth_on_ruin = capital - base * (2**bets - 1)
    expected = win * wealth_on_win + ruin * wealth_on_ruin
    return {
        "bets_allowed": bets,
        "win_probability": win,
        "ruin_probability": ruin,
        "wealth_on_win_cents": wealth_on_win,
        "wealth_on_ruin_cents": wealth_on_ruin,
        "max_stake_cents": base * 2 ** (bets - 1),
        "expected_final_wealth_cents": _nearest_cent(expected),
    }


def dyadic_martingale_error(instance: dict[str, Any], n: int) -> Fraction:
    """E[(M_n - Y)^2] for Y(x) = x on [0, 1] and M_n the average of Y over each level-n dyadic cell, exact."""
    if n < 0:
        raise ValueError("the dyadic level n must be a whole number of at least 0")
    cells = 2**n
    width = Fraction(1, cells)
    total = Fraction(0)
    for j in range(cells):
        a = Fraction(j, cells)
        b = a + width
        c = (a + b) / 2
        total += ((b - c) ** 3 - (a - c) ** 3) / 3
    return total


def dyadic_martingale_value(instance: dict[str, Any], n: int, x: Fraction) -> Fraction:
    """M_n(x): the midpoint of the level-n dyadic cell that contains x, for x in [0, 1].

    Cells are [j/2^n, (j+1)/2^n), and the last cell is closed at 1, so x = 1 lies in the last cell.
    """
    if n < 0:
        raise ValueError("the dyadic level n must be a whole number of at least 0")
    point = Fraction(x)
    if not 0 <= point <= 1:
        raise ValueError("the point x must lie in [0, 1]")
    cells = 2**n
    index = min(int(point * cells), cells - 1)  # point is in [0, 1], so truncation is the floor
    return Fraction(2 * index + 1, 2 * cells)
