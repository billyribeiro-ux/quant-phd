"""Independent recomputation of the project Lab 3 reference numbers (verifier round 1), by a different method.

Each probability is recomputed by a recursion over the distribution of the walk, not by the enumeration the lab uses.
Usage: <checkout>/.venv/bin/python ledgers/M6/scripts/M6-d-r1/lab3_recompute.py
"""

from __future__ import annotations

import math
from fractions import Fraction as F

N = 6
LEVEL = 1
CAP = 4
LAM = 3
K = 100
S = 1


def stopped_mean(p: F) -> F:
    # Distribution of the walk stopped at the first hit of LEVEL or at CAP, via a Markov recursion on (position, time).
    dist = {(0, 0): F(1)}
    total = F(0)
    for t in range(CAP):
        nxt: dict[tuple[int, int], F] = {}
        for (x, s), w in dist.items():
            for step, q in ((1, p), (-1, 1 - p)):
                y = x + step
                if y == LEVEL:
                    total += w * q * y
                else:
                    nxt[(y, s + 1)] = nxt.get((y, s + 1), F(0)) + w * q
        dist = nxt
    total += sum((w * x for (x, _), w in dist.items()), F(0))
    return total


def doob(lam: int) -> tuple[F, F]:
    # Joint law of (position, running max of |S|) by recursion, fair coin.
    state = {(0, 0): F(1)}
    for _ in range(N):
        nxt: dict[tuple[int, int], F] = {}
        for (x, m), w in state.items():
            for step in (1, -1):
                y = x + step
                key = (y, max(m, abs(y)))
                nxt[key] = nxt.get(key, F(0)) + w / 2
        state = nxt
    prob = sum((w for (_, m), w in state.items() if m >= lam), F(0))
    mean_abs = sum((abs(x) * w for (x, _), w in state.items()), F(0))
    return prob, mean_abs / lam


def doubling(p: F) -> tuple[F, int]:
    # Expected final wealth by summing over the placed bets; K + S ... the bet count is J with stakes 2^(k-1).
    J = 0
    while S * 2 ** (J + 1) <= K + S:
        J += 1
    ruin = (1 - p) ** J
    win = 1 - ruin
    expected = win * (K + S) + ruin * (K - S * (2**J - 1))
    return expected, J


def dyadic_mse(n: int) -> F:
    # E[(M_n - Y)^2] = sum over cells of width h of the second moment of Y about the cell mean, h^3/12 per cell.
    h = F(1, 2**n)
    return 2**n * h**3 / 12


def half_up(x: F) -> int:
    return math.floor(x + F(1, 2))


if __name__ == "__main__":
    fair = stopped_mean(F(1, 2))
    ctl = stopped_mean(F(1, 3))
    prob, bound = doob(LAM)
    exp_fair, J = doubling(F(1, 2))
    exp_ctl, _ = doubling(F(1, 3))
    print("stopped fair", fair, "control", ctl, "decimal", f"{float(ctl):.6f}")
    print("Doob", prob, bound, prob <= bound)
    print("bets J", J, "fair expected", exp_fair, "control expected", exp_ctl, "control cents", half_up(exp_ctl))
    print("dyadic", [dyadic_mse(n) == F(1, 12 * 4**n) for n in (0, 1, 2, 3, 10)], dyadic_mse(10))
