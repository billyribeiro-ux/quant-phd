"""Alternative correct engine A6: finite-capital doubling as an absorbing Markov chain, run by explicit matrix steps."""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any


def _check_horizon(instance: dict[str, Any]) -> int:
    n = int(instance["horizon"])
    if n < 1:
        raise ValueError("the horizon N must be at least 1")
    return n


def _rounded(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


def _chain(capital: int, base: int, p: Fraction) -> dict[str, Any]:
    # states: 'win', 'ruin', and transient (k, wealth) meaning bet k is next with that wealth
    transitions: dict[Any, dict[Any, Fraction]] = {}
    start = (1, capital)
    frontier = [start]
    seen = {start}
    while frontier:
        state = frontier.pop()
        k, wealth = state
        stake = base * 2 ** (k - 1)
        if stake > wealth:
            transitions[state] = {"ruin": Fraction(1)}
            continue
        nxt_win = "win"
        nxt_lose = (k + 1, wealth - stake)
        transitions[state] = {nxt_win: p, nxt_lose: 1 - p}
        if nxt_lose not in seen:
            seen.add(nxt_lose)
            frontier.append(nxt_lose)
    transitions["win"] = {"win": Fraction(1)}
    transitions["ruin"] = {"ruin": Fraction(1)}
    return {"start": start, "P": transitions}


def _run(capital: int, base: int, p: Fraction) -> tuple[Fraction, Fraction, int, int]:
    chain = _chain(capital, base, p)
    P = chain["P"]
    dist: dict[Any, Fraction] = {chain["start"]: Fraction(1)}
    absorbed: dict[str, Fraction] = {"win": Fraction(0), "ruin": Fraction(0)}
    ruin_wealth = None
    bets = 0
    for _ in range(200):
        if not dist:
            break
        nxt: dict[Any, Fraction] = {}
        for state, mass in dist.items():
            for target, pr in P[state].items():
                if target in absorbed:
                    absorbed[target] += mass * pr
                    if target == "ruin":
                        ruin_wealth = state[1]
                        bets = state[0] - 1
                else:
                    nxt[target] = nxt.get(target, Fraction(0)) + mass * pr
        dist = nxt
    return absorbed["win"], absorbed["ruin"], bets, ruin_wealth if ruin_wealth is not None else capital


def doubling_outcome(instance: dict[str, Any]) -> dict[str, int | Fraction]:
    capital = int(instance["capital_cents"])
    base = int(instance["base_stake_cents"])
    if capital <= 0:
        raise ValueError("the capital must be a positive number of cents")
    if base > capital:
        raise ValueError("a stake larger than the capital is not allowed")
    p = Fraction(instance["win_probability"])
    win, ruin, bets, on_ruin = _run(capital, base, p)
    expected = win * (capital + base) + ruin * on_ruin
    return {
        "bets_allowed": bets,
        "win_probability": win,
        "ruin_probability": ruin,
        "wealth_on_win_cents": capital + base,
        "wealth_on_ruin_cents": on_ruin,
        "max_stake_cents": base * 2 ** (bets - 1),
        "expected_final_wealth_cents": _rounded(expected),
    }


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


def dyadic_martingale_value(instance: dict[str, Any], n: int, x: Fraction) -> Fraction:
    cells = 2**n
    x = Fraction(x)
    j = 0
    while j + 1 < cells and Fraction(j + 1, cells) <= x:
        j += 1
    return (Fraction(j, cells) + Fraction(j + 1, cells)) / 2


def dyadic_martingale_error(instance: dict[str, Any], n: int) -> Fraction:
    return Fraction(1, 12 * 4**n)


