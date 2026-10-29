"""Verifier round 2: recompute the numbers on the E2 project page and on the changed cards (exact fractions)."""

from __future__ import annotations

from fractions import Fraction
from itertools import product


def em_discrete(n: int, a: int) -> Fraction:
    # Proposition 2.2 as written on card E2-c096: E[M] = -a + sum_{x=-a}^{a-1} (1 - F(x)^n), F(x) = (x+a+1)/(2a+1)
    total = Fraction(-a)
    for x in range(-a, a):
        F = Fraction(x + a + 1, 2 * a + 1)
        total += 1 - F**n
    return total


def em_bruteforce(n: int, a: int) -> Fraction:
    # independent check: average of the max over all (2a+1)^n error vectors, exact
    vals = range(-a, a + 1)
    s = sum(max(e) for e in product(vals, repeat=n))
    return Fraction(s, (2 * a + 1) ** n)


e = em_discrete(5, 2000)
print("card c098 discrete E[M] n=5 a=2000 exact:", e, "float:", float(e))
print("  equals 85418692002000/64048012001:", e == Fraction(85418692002000, 64048012001))
print("  rounded to 2 dp:", round(float(e), 2), "| unrounded to 8 dp:", f"{float(e):.8f}")
print("card c097 continuous a(n-1)/(n+1):", Fraction(2000 * 4, 6), float(Fraction(2000 * 4, 6)))
print("c100 shading 1333 expected profit (cents):", float(1333 - e), "| 1334 minus E[M]:", float(1334 - e))
print("c101 exact total (20000 auctions) = -20000*E[M]:", float(-20000 * e), "| round:", round(-20000 * e))
print("c101 difference 26673331 - 26620718:", 26673331 - 26620718, " / 79810 =", round(52613 / 79810, 4))
print("c102 shaded total = naive + 1334*20000:", -26620718 + 1334 * 20000, "| exact:", -26673331 + 1334 * 20000)
print("c095 E[M] two bidders errors -1,0,1:", Fraction(-1, 9) + Fraction(5, 9))
# small check of formula vs brute force
for n, a in [(2, 1), (3, 2), (2, 3)]:
    print("formula vs brute n,a", n, a, em_discrete(n, a) == em_bruteforce(n, a))
# c118/c120: profiles of 4 bidders, bids in 0..3, k = 2
hi = eq = lo = 0
for b in product(range(4), repeat=4):
    s = sorted(b, reverse=True)
    disc = s[0] + s[1]
    uni = 2 * s[2]
    if disc > uni:
        hi += 1
    elif disc == uni:
        eq += 1
    else:
        lo += 1
    # equal iff three highest equal
print("c118 counts higher, equal, lower:", hi, eq, lo)
eq3 = sum(1 for b in product(range(4), repeat=4) if (lambda s: s[0] == s[1] == s[2])(sorted(b, reverse=True)))
print("c120 profiles whose three highest bids are equal:", eq3)
