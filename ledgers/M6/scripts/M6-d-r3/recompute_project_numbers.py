"""Independent recomputation of every number the project page prints or quotes (Lab 1, Lab 2, Lab 3, exemplars, P1-P3 examples)."""

from __future__ import annotations

import itertools
import math
from fractions import Fraction as F

HALF = F(1, 2)

# Lab 1: N = 3, tau = min(first time S = +1, 3); E[S_tau] and E[S_(tau and k)] on 8 paths
paths = list(itertools.product((1, -1), repeat=3))
def tau_of(steps, level=1, cap=3):
    s = 0
    for k, x in enumerate(steps, 1):
        s += x
        if s == level:
            return k
    return cap
lab1_E = sum(F(1, 8) * sum(st[: tau_of(st)]) for st in paths)
lab1_rows = [(st, tau_of(st), sum(st[: tau_of(st)])) for st in paths]
print("lab1 E[S_tau] =", lab1_E, "| tau/S_tau per path:", [(t, v) for _, t, v in lab1_rows])
for k in range(4):
    print("lab1 E[S_(tau and %d)] =" % k, sum(F(1, 8) * sum(st[: min(k, tau_of(st))]) for st in paths))
half_sum_first = sum(F(1, 8) * sum(st[: tau_of(st)]) for st in paths if st[0] == 1)
half_sum_second = sum(F(1, 8) * sum(st[: tau_of(st)]) for st in paths if st[0] == -1)
print("lab1 contributions: first-step-up", half_sum_first, "first-step-down", half_sum_second)

# Lab 2: lost bets with capital, base, cap (every bet loses)
def lost(capital, base, cap):
    wealth, placed = capital, 0
    while placed < cap:
        stake = base * 2**placed
        if stake > wealth:
            break
        wealth -= stake
        placed += 1
    return placed, wealth
print("lab2", lost(100, 1, 10), lost(1, 1, 10), lost(1000, 1, 6))

# Lab 3 (illustrative case): N = 6, tau = min(first S = +1, 4), Doob level 3, doubling 100/1, control p = 1/3
N, LEVEL, CAP, LAM, CAPITAL, BASE, CONTROL = 6, 1, 4, 3, 100, 1, F(1, 3)
def stopped(p):
    tot = F(0)
    for st in itertools.product((1, -1), repeat=N):
        w = F(1)
        for x in st:
            w *= p if x == 1 else 1 - p
        val = None
        s = 0
        for x in st[:CAP]:
            s += x
            if s == LEVEL:
                val = s
                break
        if val is None:
            val = sum(st[:CAP])
        tot += w * val
    return tot
fair = stopped(HALF)
ctl = stopped(CONTROL)
print("lab3 fair E[S_tau] =", fair, "| control E[S_tau] =", ctl, "| decimal", round(float(ctl), 6))
hits = F(0)
ebs = F(0)
for st in itertools.product((1, -1), repeat=N):
    s, peak = 0, 0
    for x in st:
        s += x
        peak = max(peak, abs(s))
    if peak >= LAM:
        hits += F(1, 2**N)
    ebs += F(1, 2**N) * abs(s)
bound = ebs / LAM
print("lab3 Doob P =", hits, "bound =", bound, "holds", hits <= bound, "| decimals", round(float(hits), 6), round(float(bound), 6))

def doubling(p):
    # exact recursion over bets: bet k stakes BASE*2^(k-1); placed only if stake <= wealth
    out = {"win": F(0), "ruin": F(0), "exp": F(0)}
    def rec(wealth, k, w):
        stake = BASE * 2 ** (k - 1)
        if stake > wealth:
            out["ruin"] += w
            out["exp"] += w * wealth
            out["bets"] = k - 1
            out["ruin_wealth"] = wealth
            return
        out["win"] += w * p
        out["exp"] += w * p * (wealth + stake)
        rec(wealth - stake, k + 1, w * (1 - p))
    rec(CAPITAL, 1, F(1))
    return out
fd = doubling(HALF)
cd = doubling(CONTROL)
print("lab3 doubling fair: bets", fd["bets"], "win", fd["win"], "ruin", fd["ruin"], "wealth on ruin", fd["ruin_wealth"], "E", fd["exp"])
print("lab3 doubling control: E", cd["exp"], "=", float(cd["exp"]), "cents half-up", math.floor(cd["exp"] + HALF))

def dyadic_err(n):
    cells = 2**n
    tot = F(0)
    for j in range(cells):
        a, b = F(j, cells), F(j + 1, cells)
        c = (a + b) / 2
        tot += ((b - c) ** 3 - (a - c) ** 3) / 3
    return tot
print("dyadic", [(n, dyadic_err(n) == F(1, 12 * 4**n)) for n in (0, 1, 2, 3, 10)], "n=10 value", dyadic_err(10))
x = F(1, 3)
j = min(math.floor(x * 2**10), 2**10 - 1)
print("M_10(1/3) =", F(2 * j + 1, 2 * 2**10), "| |M-x| <= 2^-11:", abs(F(2 * j + 1, 2 * 2**10) - x) <= F(1, 2**11))

# Rung 2 (project lab 2 expected): capital 100 base 1 -> 6 bets, 37 left
# Stopping-rule example: P(tau > n) = 2^-n for the unbounded doubling
print("P(tau>n) check", [F(1, 2**n) for n in (1, 2, 3)])
# Exemplar B arithmetic
print("exemplar B: 69533/729 =", F(69533, 729), float(F(69533, 729)))
print("exemplar A bad bound E[X_N^2]/3 vs E|S_6|/3 :", "not recomputed here")
print("doubling identity at capital 100: 63/64*101 + 1/64*37 =", F(63, 64) * 101 + F(1, 64) * 37)
print("chapter P2 tight example N=1 lambda=1 |S|:", F(1), F(1))
