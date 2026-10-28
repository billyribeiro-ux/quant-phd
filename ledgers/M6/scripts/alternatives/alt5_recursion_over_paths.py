"""Alternative 5: recursion over the bets for doubling, a recursion over the paths for the walks, and the closed form."""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any


def _paths(length: int) -> list[tuple[int, ...]]:
    """Every coin sequence of the given length, as tuples of +1 and -1."""
    if length == 0:
        return [()]
    return [(step,) + rest for step in (1, -1) for rest in _paths(length - 1)]


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
    for path in _paths(horizon):
        weight = Fraction(1)
        for step in path:
            weight *= p if step == 1 else 1 - p
        running = 0
        for k in range(cap):
            running += path[k]
            if running == level:
                break
        total += weight * running
    return total


def doob_max_probability(instance: dict[str, Any], lam: int) -> tuple[Fraction, Fraction]:
    horizon = int(instance["horizon"])
    if horizon < 1:
        raise ValueError("the horizon N must be at least 1 step")
    if lam <= 0:
        raise ValueError("the level lambda in Doob's inequality must be a positive number of steps")
    weight = Fraction(1, 2**horizon)
    hit = Fraction(0)
    mean_abs = Fraction(0)
    for path in _paths(horizon):
        running = 0
        peak = 0
        for step in path:
            running += step
            peak = max(peak, abs(running))
        if peak >= lam:
            hit += weight
        mean_abs += weight * abs(running)
    return hit, mean_abs / lam


def _bets(capital: int, base: int, p: Fraction, bet: int, wealth: int) -> tuple[Fraction, Fraction, Fraction, int]:
    """(win probability, ruin probability, expected wealth from here, bets placed from here) by recursion."""
    stake = base * 2 ** (bet - 1)
    if stake > wealth:
        return Fraction(0), Fraction(1), Fraction(wealth), 0
    w_win, w_ruin, e_rest, n_rest = _bets(capital, base, p, bet + 1, wealth - stake)
    win = p + (1 - p) * w_win
    ruin = (1 - p) * w_ruin
    expected = p * (wealth + stake) + (1 - p) * e_rest
    return win, ruin, expected, n_rest + 1


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
    win, ruin, expected, bets = _bets(capital, base, p, 1, capital)
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
