"""Round 10: enumerate L05 Problem R1 (n trades, equal delay l, cost k per day) for n = 2..4 under A3 and A4.

Checks E[C] = n p k l under both laws, and Var_4 / Var_3 = n. Run with python3 -I -W error from any directory.
"""

import itertools
from fractions import Fraction as F


def stats(n, p, k, l):
    outs3 = []
    for pat in itertools.product((0, 1), repeat=n):
        pr = F(1)
        for f in pat:
            pr *= p if f else (1 - p)
        outs3.append((pr, k * l * sum(pat)))
    outs4 = [(1 - p, 0), (p, k * l * n)]

    def mv(outs):
        m = sum(pr * c for pr, c in outs)
        v = sum(pr * c * c for pr, c in outs) - m * m
        return m, v

    return mv(outs3), mv(outs4)


for n in (2, 3, 4):
    for p, k, l in ((F(1, 8), 2500, 2), (F(1, 4), 1000, 3)):
        (m3, v3), (m4, v4) = stats(n, p, k, l)
        print(f"n={n} p={p} k={k} l={l}: mean3={m3} mean4={m4} formula={n * p * k * l} "
              f"ratio={v4 / v3} ok={m3 == m4 == n * p * k * l and v4 / v3 == n}")
