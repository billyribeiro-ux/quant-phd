"""Alternative engine A5 (time-zero convention, tau = first k >= 0 with S_k = level), a variant of A2: every quantity by enumerating the 2^N paths or the bet sequences, no recursion."""

from __future__ import annotations

import itertools
import math
from fractions import Fraction
from typing import Any


def _n(instance: dict[str, Any]) -> int:
    n = int(instance["horizon"])
    if n < 1:
        raise ValueError("the horizon N must be at least 1")
    return n


def _weight(steps: tuple[int, ...], p: Fraction) -> Fraction:
    w = Fraction(1)
    for s in steps:
        w *= p if s == 1 else (1 - p)
    return w


def stopped_value_expectation(instance: dict[str, Any]) -> Fraction:
    n = _n(instance)
    level = int(instance["stop_level"])
    cap = int(instance["stop_cap"])
    if cap > n:
        raise ValueError("the stopping rule is not bounded by N")
    p = Fraction(instance["win_probability"])
    if level == 0:
        # convention k >= 0: tau = 0 when the walk starts at the stopping level, so S_tau = 0 on every path
        return Fraction(0)
    total = Fraction(0)
    for steps in itertools.product((1, -1), repeat=n):
        pos = 0
        tau = cap
        for k in range(1, cap + 1):
            pos += steps[k - 1]
            if pos == level:
                tau = k
                break
        total += _weight(steps, p) * sum(steps[:tau])
    return total


def doob_max_probability(instance: dict[str, Any], lam: int) -> tuple[Fraction, Fraction]:
    n = _n(instance)
    if lam <= 0:
        raise ValueError("lambda must be positive")
    half = Fraction(1, 2)
    hit = Fraction(0)
    mean = Fraction(0)
    for steps in itertools.product((1, -1), repeat=n):
        pos = 0
        peak = 0
        for s in steps:
            pos += s
            peak = max(peak, abs(pos))
        if peak >= lam:
            hit += half**n
        mean += half**n * abs(pos)
    return hit, mean / lam


def doubling_outcome(instance: dict[str, Any]) -> dict[str, int | Fraction]:
    capital = int(instance["capital_cents"])
    base = int(instance["base_stake_cents"])
    if capital <= 0:
        raise ValueError("the capital must be positive")
    if base > capital:
        raise ValueError("a stake larger than the capital is not allowed")
    p = Fraction(instance["win_probability"])
    length = 1
    while base * 2 ** (length - 1) <= capital + base:
        length += 1  # every bet index that can be placed or can trigger ruin is <= length
    win = Fraction(0)
    ruin = Fraction(0)
    expected = Fraction(0)
    bets_placed = None
    wins_on = {}
    ruin_on = {}
    for seq in itertools.product((1, -1), repeat=length):
        w = _weight(seq, p)  # full-length weight: each stopping event is counted once, its extensions sum to 1
        wealth = capital
        for k, s in enumerate(seq, start=1):
            stake = base * 2 ** (k - 1)
            if stake > wealth:
                ruin += w
                expected += w * wealth
                ruin_on[k - 1] = wealth
                bets_placed = k - 1 if bets_placed is None else bets_placed
                break
            if s == 1:
                win += w
                expected += w * (wealth + stake)
                break
            wealth -= stake
    cents = math.floor(expected + Fraction(1, 2))
    placed_out = bets_placed if bets_placed is not None else 0
    return {
        "bets_allowed": placed_out,
        "win_probability": win,
        "ruin_probability": ruin,
        "wealth_on_win_cents": capital + base,
        "wealth_on_ruin_cents": capital - base * (2**placed_out - 1),
        "max_stake_cents": base * 2 ** (placed_out - 1),
        "expected_final_wealth_cents": cents,
    }


def dyadic_martingale_error(instance: dict[str, Any], n: int) -> Fraction:
    # within a cell of width h, Y is uniform on the cell, so E[(Y - mean)^2 | cell] = h^2/12; the cell has probability h
    h = Fraction(1, 2**n)
    return 2**n * h * (h * h / 12)


def dyadic_martingale_value(instance: dict[str, Any], n: int, x: Fraction) -> Fraction:
    cells = 2**n
    x = Fraction(x)
    for j in range(cells):
        lo, hi = Fraction(j, cells), Fraction(j + 1, cells)
        if lo <= x < hi or (j == cells - 1 and x == hi):
            return (lo + hi) / 2
    raise ValueError("the point x must lie in [0, 1]")
