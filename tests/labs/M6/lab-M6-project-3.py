"""Rung 3 reference numbers: the values the report quotes for one illustrative case of each martingale check.

Standard library only. Everything is exact: each probability and expectation is a fractions.Fraction computed by
enumeration or by a closed sum, and each money amount is an integer number of cents, rounded once, half up, from the
exact value. The case is illustrative and is not a generated instance: a walk of horizon N = 6, a stopping rule
tau = min(first time S = +1, 4), Doob's level 3, doubling with capital 100 cents and base stake 1 cent, the dyadic
martingale for levels 0, 1, 2, 3 and 10, and a biased control with win probability 1/3. Copy this file into
report/run_report.py, then replace the enumerations with calls to your martingale_checks module. It must print the same
lines.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction

HALF = Fraction(1, 2)
HORIZON = 6
LEVEL = 1
CAP = 4
LAM = 3
CAPITAL = 100
BASE = 1
CONTROL = Fraction(1, 3)


def half_up(amount: Fraction) -> int:
    """An exact amount in cents, rounded once, half up: floor(x + 1/2)."""
    return math.floor(amount + HALF)


def stopped_expectation(p: Fraction) -> Fraction:
    """E[S_tau] for tau = min(first time S = LEVEL, CAP), by enumerating the 2**HORIZON paths."""
    total = Fraction(0)
    for steps in itertools.product((1, -1), repeat=HORIZON):
        weight = Fraction(1)
        for step in steps:
            weight *= p if step == 1 else 1 - p
        position = 0
        value = None
        for step in steps[:CAP]:
            position += step
            if position == LEVEL:
                value = position
                break
        if value is None:
            value = sum(steps[:CAP])
        total += weight * value
    return total


def doob(lam: int) -> tuple[Fraction, Fraction]:
    """P(max over k <= HORIZON of |S_k| >= lam) and E|S_HORIZON| / lam for the fair walk, by enumeration."""
    hits = Fraction(0)
    expected_abs = Fraction(0)
    weight = Fraction(1, 2**HORIZON)
    for steps in itertools.product((1, -1), repeat=HORIZON):
        position = 0
        peak = 0
        for step in steps:
            position += step
            peak = max(peak, abs(position))
        if peak >= lam:
            hits += weight
        expected_abs += weight * abs(position)
    return hits, expected_abs / lam


def doubling(p: Fraction) -> dict[str, Fraction | int]:
    """Doubling with CAPITAL cents and base stake BASE: bets placed, probabilities, wealths and E[final], exact.

    A bet is placed while its stake does not exceed the wealth on hand. The strategy stops at the first win, which
    leaves CAPITAL + BASE, or at ruin, after the placed bets have all lost.
    """
    branches: list[tuple[Fraction, int, str, int]] = []

    def play(wealth: int, bet: int, weight: Fraction) -> None:
        stake = BASE * 2 ** (bet - 1)
        if stake > wealth:
            branches.append((weight, wealth, "ruin", bet - 1))
            return
        branches.append((weight * p, wealth + stake, "win", bet))
        play(wealth - stake, bet + 1, weight * (1 - p))

    play(CAPITAL, 1, Fraction(1))
    win = sum((w for w, _, kind, _ in branches if kind == "win"), Fraction(0))
    ruin = sum((w for w, _, kind, _ in branches if kind == "ruin"), Fraction(0))
    expected = sum((w * wealth for w, wealth, _, _ in branches), Fraction(0))
    placed = next(bets for _, _, kind, bets in branches if kind == "ruin")
    return {
        "bets": placed,
        "win": win,
        "ruin": ruin,
        "wealth_on_win": CAPITAL + BASE,
        "wealth_on_ruin": CAPITAL - BASE * (2**placed - 1),
        "expected": expected,
        "expected_cents": half_up(expected),
    }


def dyadic_error(n: int) -> Fraction:
    """E[(M_n - Y)^2] for Y(x) = x on [0, 1]: the sum over the 2**n cells of the exact integral of (x - midpoint)^2."""
    cells = 2**n
    width = Fraction(1, cells)
    total = Fraction(0)
    for j in range(cells):
        a = Fraction(j, cells)
        b = a + width
        c = (a + b) / 2
        total += ((b - c) ** 3 - (a - c) ** 3) / 3
    return total


def dyadic_value(n: int, x: Fraction) -> Fraction:
    """M_n(x): the midpoint of the level-n cell that contains x, for x in [0, 1]."""
    cells = 2**n
    index = min(int(x * cells), cells - 1)  # x is in [0, 1], so truncation is the floor
    return Fraction(2 * index + 1, 2 * cells)


def main() -> None:
    """Print the reference values for the four checks, the control and the dyadic martingale."""
    fair = stopped_expectation(HALF)
    control = stopped_expectation(CONTROL)
    print("stopped walk, fair coin: E[S_tau] =", fair)
    print("stopped walk, control p = 1/3: E[S_tau] =", control, "| decimal", f"{float(control):.6f}")
    prob, bound = doob(LAM)
    print(f"Doob, N = {HORIZON}, level {LAM}: P(max |S_k| >= {LAM}) =", prob, "| bound E|S_N|/level =", bound)
    print("Doob bound decimal", f"{float(bound):.6f}", "| probability decimal", f"{float(prob):.6f}")
    print("Doob holds:", prob <= bound)
    fair_out = doubling(HALF)
    print(
        f"doubling, capital {CAPITAL}, base {BASE}, fair coin: bets {fair_out['bets']}, "
        f"P(win) = {fair_out['win']}, P(ruin) = {fair_out['ruin']}, "
        f"wealth on win {fair_out['wealth_on_win']}, wealth on ruin {fair_out['wealth_on_ruin']}"
    )
    print("doubling, fair coin: E[final wealth] =", fair_out["expected"], "| cents", fair_out["expected_cents"])
    control_out = doubling(CONTROL)
    print(
        "doubling, control p = 1/3: E[final wealth] =",
        control_out["expected"],
        "| decimal",
        f"{float(control_out['expected']):.6f}",
        "| cents",
        control_out["expected_cents"],
    )
    for n in (0, 1, 2, 3, 10):
        print(
            f"dyadic level {n}: E[(M_n - Y)^2] =",
            dyadic_error(n),
            "| closed form equal:",
            dyadic_error(n) == Fraction(1, 12 * 4**n),
        )
    x = Fraction(1, 3)
    print(
        "dyadic level 10 at x = 1/3: M_10(x) =",
        dyadic_value(10, x),
        "| |M_10(x) - x| <= 2**-11:",
        abs(dyadic_value(10, x) - x) <= Fraction(1, 2**11),
    )


main()
