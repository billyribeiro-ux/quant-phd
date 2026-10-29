"""Alternative correct engine A1: list-based distribution DP with absorbing barrier, cumulative-count Doob, cell-integral dyadic."""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any


def _check_horizon(instance: dict[str, Any]) -> int:
    n = int(instance["horizon"])
    if n < 1:
        raise ValueError("horizon")
    return n


def stopped_value_expectation(instance: dict[str, Any]) -> Fraction:
    n = _check_horizon(instance)
    level = int(instance["stop_level"])
    cap = int(instance["stop_cap"])
    if cap > n:
        raise ValueError("cap above horizon")
    p = Fraction(instance["win_probability"])
    width = 2 * n + 1
    off = n  # index = position + off
    dist = [Fraction(0)] * width
    dist[off] = Fraction(1)
    total = Fraction(0)
    for _ in range(cap):
        new = [Fraction(0)] * width
        for i, w in enumerate(dist):
            if w == 0:
                continue
            for step, q in ((1, p), (-1, 1 - p)):
                j = i + step
                if j - off == level:
                    total += w * q * level
                else:
                    new[j] += w * q
        dist = new
    for i, w in enumerate(dist):
        total += w * (i - off)
    return total


def doob_max_probability(instance: dict[str, Any], lam: int) -> tuple[Fraction, Fraction]:
    n = _check_horizon(instance)
    if lam <= 0:
        raise ValueError("level")
    half = Fraction(1, 2)
    # state: (position, max |S| so far) as a dict; the probability of reaching lam is the mass with max >= lam
    states: dict[tuple[int, int], Fraction] = {(0, 0): Fraction(1)}
    for _ in range(n):
        nxt: dict[tuple[int, int], Fraction] = {}
        for (pos, peak), w in states.items():
            for step in (1, -1):
                q = pos + step
                key = (q, max(peak, abs(q)))
                nxt[key] = nxt.get(key, Fraction(0)) + w * half
        states = nxt
    hit = sum((w for (_, peak), w in states.items() if peak >= lam), Fraction(0))
    mean_abs = sum((abs(pos) * w for (pos, _), w in states.items()), Fraction(0))
    return hit, mean_abs / lam


def doubling_outcome(instance: dict[str, Any]) -> dict[str, int | Fraction]:
    capital = int(instance["capital_cents"])
    base = int(instance["base_stake_cents"])
    if capital <= 0:
        raise ValueError("capital")
    if base > capital:
        raise ValueError("stake")
    p = Fraction(instance["win_probability"])
    # walk the bets: wealth before bet k is capital - base*(2^(k-1)-1) while every bet loses
    k = 1
    wealth = capital
    while base * 2 ** (k - 1) <= wealth:
        wealth -= base * 2 ** (k - 1)
        k += 1
    placed = k - 1
    ruin = (1 - p) ** placed
    win = 1 - ruin
    on_win = capital + base
    on_ruin = wealth
    expected = win * on_win + ruin * on_ruin
    cents = math.floor(expected + Fraction(1, 2))
    return {
        "bets_allowed": placed,
        "win_probability": win,
        "ruin_probability": ruin,
        "wealth_on_win_cents": on_win,
        "wealth_on_ruin_cents": on_ruin,
        "max_stake_cents": base * 2 ** (placed - 1),
        "expected_final_wealth_cents": cents,
    }


def dyadic_martingale_error(instance: dict[str, Any], n: int) -> Fraction:
    cells = 2**n
    total = Fraction(0)
    for j in range(cells):
        lo = Fraction(j, cells)
        hi = Fraction(j + 1, cells)
        mid = (lo + hi) / 2
        # integral over the cell of (x - mid)^2 dx, by the antiderivative of the square
        total += Fraction(1, cells) * 0 + ((hi - mid) ** 3 - (lo - mid) ** 3) / 3
    return total


def dyadic_martingale_value(instance: dict[str, Any], n: int, x: Fraction) -> Fraction:
    cells = 2**n
    x = Fraction(x)
    j = 0
    while j + 1 < cells and Fraction(j + 1, cells) <= x:
        j += 1
    return (Fraction(j, cells) + Fraction(j + 1, cells)) / 2
