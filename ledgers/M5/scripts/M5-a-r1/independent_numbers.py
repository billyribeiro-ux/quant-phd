"""Independent exact re-derivation of the numbers printed or claimed on hub and lessons L01-L04.

Usage: python3 -I ledgers/M5/scripts/M5-a-r1/independent_numbers.py
Exact rational arithmetic throughout (fractions.Fraction).
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product


def main() -> None:
    half, thousandth, kilo = Fraction(1, 2), Fraction(1, 1000), Fraction(1, 1024)
    # L01: bisection on S = {x >= 0 : x*x < 2} from [0, 2], 12 steps
    a, b = Fraction(0), Fraction(2)
    brackets = [(a, b)]
    for _ in range(12):
        m = (a + b) / 2
        if m >= 0 and m * m < 2:
            a = m
        else:
            b = m
        brackets.append((a, b))
    print("L01 step-12 bracket", brackets[12][0], brackets[12][1], "width", brackets[12][1] - brackets[12][0])
    print("L01 sandwich count", sum(x * x < 2 <= y * y for x, y in brackets), "of", len(brackets))
    print("L01 first step with width < 1/1000", next(n for n, (x, y) in enumerate(brackets) if y - x < thousandth))
    print("L01 E1 squares", 181**2, 2 * 128**2, 2897**2, 2 * 2048**2)
    # L02: harmonic gaps and the geometric test
    harmonic = [Fraction(0)]
    for k in range(1, 401):
        harmonic.append(harmonic[-1] + Fraction(1, k))
    gaps = [harmonic[2 * n] - harmonic[n] for n in range(1, 201)]
    print(
        "L02 gaps >= 1/2:", sum(g >= half for g in gaps), "of 200; min", min(gaps), "at N =", gaps.index(min(gaps)) + 1
    )
    geometric = [Fraction(0)]
    for k in range(1, 61):
        geometric.append(geometric[-1] + Fraction(1, 2**k))
    pairs = [(n, m) for n in range(60) for m in range(n + 1, 61)]
    identity = sum(geometric[m] - geometric[n] == Fraction(1, 2**n) - Fraction(1, 2**m) for n, m in pairs)
    print("L02 identity holds on", identity, "of", len(pairs), "pairs")

    def fails_from(start: int) -> bool:
        return any(abs(geometric[m] - geometric[n]) >= kilo for n in range(start, 61) for m in range(n + 1, 61))

    print("L02 test fails for N in 0..20:", [n for n in range(21) if fails_from(n)])
    # L03: grid 2 + k/200 for |k| <= 200
    grid = [Fraction(2) + Fraction(k, 200) for k in range(-200, 201)]
    print("L03 bound holds at", sum(abs(x * x - 4) <= 5 * abs(x - 2) for x in grid), "of", len(grid))
    tenth = Fraction(1, 10)
    inside = [x for x in grid if abs(x - 2) < Fraction(1, 50)]
    print("L03 delta = 1/50 admits", len(inside), "; all good:", all(abs(x * x - 4) < tenth for x in inside))
    bad = [x for x in grid if abs(x - 2) < tenth and abs(x * x - 4) >= tenth]
    print("L03 delta = 1/10 bad count", len(bad), "; first", bad[0], "with |x^2-4| =", abs(bad[0] * bad[0] - 4))
    # L04: squared distance on {0, 1, 2}
    failing = [(x, y, z) for x, y, z in product([0, 1, 2], repeat=3) if (x - z) ** 2 > (x - y) ** 2 + (y - z) ** 2]
    print("L04 squared-distance triangle failures:", failing)
    print("L04 Part A pairs/triples", 25**2, 25**3, "Part B pairs/triples", 27**2, 27**3)

    # Extra numbers quoted on the pages
    print("L01 Q5 squares", Fraction(7, 5) ** 2, Fraction(141, 100) ** 2, Fraction(141, 100) > Fraction(7, 5))
    print("L02 E2 H4-H2", harmonic[4] - harmonic[2], "G3", geometric[3], "G3-G1", geometric[3] - geometric[1])
    k_pos = [k for k in range(1, 20) if k * (4 + Fraction(k, 200)) >= 20]
    j_neg = [j for j in range(1, 20) if j * (4 - Fraction(j, 200)) >= 20]
    print("L03 E3 counts", len(k_pos), min(k_pos), len(j_neg), min(j_neg), len(k_pos) + len(j_neg))
    print("L03 E1 bound at 381/200", 5 * abs(Fraction(381, 200) - 2), abs(Fraction(381, 200) ** 2 - 4))
    print("L04 mech3 sup of x - x^2 on grid", max(Fraction(i, 1000) - (Fraction(i, 1000)) ** 2 for i in range(1001)))
    print(
        "hub placement 7/9, 8/9 as percent",
        round(7 / 9 * 100, 1),
        round(8 / 9 * 100, 1),
        "sum 1+1/2+1/4+1/8+1/16",
        1 + Fraction(1, 2) + Fraction(1, 4) + Fraction(1, 8) + Fraction(1, 16),
    )
    print(
        "hub rung-2 bound",
        Fraction(1, 2) * 4,
        "hub rung-1 example bound beta/(1-beta)*0.2",
        Fraction(9, 10) / (1 - Fraction(9, 10)) * Fraction(1, 5),
    )


if __name__ == "__main__":
    main()
