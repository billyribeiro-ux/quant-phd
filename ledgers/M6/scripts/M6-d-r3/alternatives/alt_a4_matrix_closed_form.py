"""Alternative correct engine A4: closed forms and integer rounding with a different cutoff (numerator arithmetic)."""

from __future__ import annotations

from fractions import Fraction
from typing import Any


def _rounded_half_up(x: Fraction) -> int:
    num, den = x.numerator, x.denominator
    return (2 * num + den) // (2 * den)  # floor(x + 1/2) computed in integers


def stopped_value_expectation(instance: dict[str, Any]) -> Fraction:
    n = int(instance["horizon"])
    if n < 1:
        raise ValueError("the horizon N must be at least 1")
    level = int(instance["stop_level"])
    cap = int(instance["stop_cap"])
    if cap > n:
        raise ValueError("the stopping rule is not bounded by N")
    p = Fraction(instance["win_probability"])
    q = 1 - p
    # transition matrix on the states (position) for cap steps, absorbing at level (level is never 0 except in tests)
    offset = cap
    size = 2 * cap + 1
    vec = [Fraction(0)] * size
    vec[offset] = Fraction(1)
    total = Fraction(0)
    for step_index in range(cap):
        out = [Fraction(0)] * size
        for i in range(size):
            if vec[i] == 0:
                continue
            for d, pr in ((1, p), (-1, q)):
                j = i + d
                pos = j - offset
                if step_index >= 0 and pos == level and step_index + 1 >= 1:
                    total += vec[i] * pr * pos
                elif 0 <= j < size:
                    out[j] += vec[i] * pr
        vec = out
    total += sum((vec[i] * (i - offset) for i in range(size)), Fraction(0))
    return total


def doob_max_probability(instance: dict[str, Any], lam: int) -> tuple[Fraction, Fraction]:
    n = int(instance["horizon"])
    if n < 1:
        raise ValueError("the horizon N must be at least 1")
    if lam <= 0:
        raise ValueError("lambda must be positive")
    # count the fair walk's paths by integer binomial sums: a path reaches lam iff its peak is at least lam
    from math import comb

    total = 2**n
    hit = 0
    # reflection principle is not used; count by brute recursion on (pos, reached) with integers
    layer = {(0, False): 1}
    for _ in range(n):
        nxt: dict[tuple[int, bool], int] = {}
        for (x, r), c in layer.items():
            for y in (x + 1, x - 1):
                key = (y, r or abs(y) >= lam)
                nxt[key] = nxt.get(key, 0) + c
        layer = nxt
    hit = sum(c for (_, r), c in layer.items() if r)
    mean_abs_num = sum(abs(x) * c for (x, _), c in layer.items())
    del comb
    return Fraction(hit, total), Fraction(mean_abs_num, total * lam)


def doubling_outcome(instance: dict[str, Any]) -> dict[str, int | Fraction]:
    capital = int(instance["capital_cents"])
    base = int(instance["base_stake_cents"])
    if capital <= 0:
        raise ValueError("the capital must be a positive number of cents")
    if base > capital:
        raise ValueError("a stake larger than the capital is not allowed")
    p = Fraction(instance["win_probability"])
    k = 1
    while base * 2**k <= capital + base:
        k += 1
    bets = k - 1
    ruin = (1 - p) ** bets
    win = 1 - ruin
    on_ruin = capital - base * (2**bets - 1)
    expected = win * (capital + base) + ruin * on_ruin
    return {
        "bets_allowed": bets,
        "win_probability": win,
        "ruin_probability": ruin,
        "wealth_on_win_cents": capital + base,
        "wealth_on_ruin_cents": on_ruin,
        "max_stake_cents": base * 2 ** (bets - 1),
        "expected_final_wealth_cents": _rounded_half_up(expected),
    }


def dyadic_martingale_error(instance: dict[str, Any], n: int) -> Fraction:
    return Fraction(1, 12 * 4**n)


def dyadic_martingale_value(instance: dict[str, Any], n: int, x: Fraction) -> Fraction:
    x = Fraction(x)
    if not 0 <= x <= 1:
        raise ValueError("x in [0, 1]")
    cells = 2**n
    index = int(x * cells)
    if index == cells:
        index = cells - 1
    return Fraction(2 * index + 1, 2 * cells)
