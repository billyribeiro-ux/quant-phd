"""Verifier round 1: brute-force grid check of Propositions 2 and 3 (equilibria) for small valid inputs.

Bertrand: fees on the grid k/N in [0, a/b]; the lower fee takes the whole demand a - b f, a tie splits it.
Cournot: quantities on the grid k/N in [0, a]; profit of exchange i is ((a - q_i - q_j)/b - c) q_i.
Each grid profile is tested for being a Nash equilibrium on the grid (no grid deviation gains).
"""

from __future__ import annotations

from fractions import Fraction as F

def profit_bertrand(f_own: F, f_rival: F, a: int, b: int, c: int) -> F:
    if f_own < f_rival:
        share = F(1)
    elif f_own == f_rival:
        share = F(1, 2)
    else:
        share = F(0)
    demand = F(a) - b * f_own
    if demand <= 0:
        return F(0)
    return (f_own - c) * demand * share

def check_bertrand(a: int, b: int, c: int, N: int) -> list[tuple[F, F]]:
    grid = [F(k, N) for k in range(0, a * N // b + 1)]
    eqs: list[tuple[F, F]] = []
    for f1 in grid:
        for f2 in grid:
            p1, p2 = profit_bertrand(f1, f2, a, b, c), profit_bertrand(f2, f1, a, b, c)
            ok = True
            for g in grid:
                if profit_bertrand(g, f2, a, b, c) > p1:
                    ok = False
                    break
            if ok:
                for g in grid:
                    if profit_bertrand(g, f1, a, b, c) > p2:
                        ok = False
                        break
            if ok:
                eqs.append((f1, f2))
    return eqs

def profit_cournot(q_own: F, q_rival: F, a: int, b: int, c: int) -> F:
    return ((F(a) - q_own - q_rival) / b - c) * q_own

def check_cournot(a: int, b: int, c: int, N: int) -> list[tuple[F, F]]:
    grid = [F(k, N) for k in range(0, a * N + 1)]
    eqs: list[tuple[F, F]] = []
    for q1 in grid:
        for q2 in grid:
            ok = all(profit_cournot(g, q2, a, b, c) <= profit_cournot(q1, q2, a, b, c) for g in grid) and all(
                profit_cournot(g, q1, a, b, c) <= profit_cournot(q2, q1, a, b, c) for g in grid)
            if ok:
                eqs.append((q1, q2))
    return eqs

if __name__ == "__main__":
    for a, b, c, N in [(12, 1, 3, 6), (10, 2, 2, 4), (13, 3, 1, 3), (9, 1, 4, 4)]:
        eq_b = check_bertrand(a, b, c, N)
        d = F(a - b * c)
        print(f"bertrand a={a} b={b} c={c} grid N={N}: equilibria on grid = {eq_b}; (c,c) is {(F(c), F(c)) in eq_b}")
        eq_c = check_cournot(a, b, c, N)
        print(f"cournot a={a} b={b} c={c} grid N={N}: equilibria on grid = {eq_c}; d/3 = {d / 3} (on grid: {d / 3 * N == int(d / 3 * N)})")
