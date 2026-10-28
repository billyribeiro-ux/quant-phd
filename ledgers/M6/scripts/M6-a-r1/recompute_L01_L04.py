"""Independent recomputation for M6 slice a (L01-L04, hub numbers). Written by verifier; standard library only."""
from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import product
import math

getcontext().prec = 50

# L03: I_n = sum_k (k/2^n)(sqrt((k+1)/2^n) - sqrt(k/2^n)), error = 1/3 - I_n, bound 2^-n
third = Decimal(1) / Decimal(3)
def I(n):
    s = Decimal(2) ** n
    tot = Decimal(0)
    for k in range(2 ** n):
        a = Decimal(k) / s
        b = Decimal(k + 1) / s
        tot += a * (b.sqrt() - a.sqrt())
    return tot
prev = None
for n in range(1, 11):
    v = I(n)
    err = third - v
    bound = Decimal(1) / (Decimal(2) ** n)
    ok = Decimal(0) <= err <= bound
    print(f"L03 n={n:2d} I_n={float(v):.10f} err={float(err):.10f} bound={float(bound):.10f} inside={ok}")
    assert ok
    if prev is not None:
        assert v >= prev
    prev = v
print("L03 I_1 closed form 0.5*(1-sqrt(1/2)) =", float(Decimal("0.5") * (1 - Decimal("0.5").sqrt())))
print("L03 I_2 terms:", [float(Decimal(k)/4 * (Decimal(k+1)/4).sqrt() - Decimal(k)/4 * (Decimal(k)/4).sqrt()) for k in (1,2,3)])
# unrounded misconception: 1/3 - I_1 ~ 0.1869
print("L03 gap 1/3 - I_1 =", float(third - I(1)))

# L04: partial sums of 1/(n+1)
s10 = sum(Fraction(1, n + 1) for n in range(1, 11))
s100 = sum(Fraction(1, n + 1) for n in range(1, 101))
print("L04 sum n=1..10 of 1/(n+1) =", float(s10), " n=1..100 =", float(s100))
# grouping bound m=1..10
for m in range(1, 11):
    assert sum(Fraction(1, k) for k in range(2, 2 ** m + 1)) >= Fraction(m, 2)
print("L04 grouping ok")
# Example 3.2: int_0^1 min(n, x^-1/2) dx = 2 - 1/n (closed form check at several n)
for n in (1, 2, 5, 10):
    closed = Decimal(1) / n + (Decimal(2) - Decimal(2) / n)
    print("L04 Ex3.2 n", n, "closed form", closed, "= 2-1/n", Decimal(2) - Decimal(1) / n)
# M3 capped power: 2*(1/4) + [2 sqrt x]_{1/4}^1 = 3/2
print("L04 M3 =", Fraction(2, 4) + (2 - 2 * Fraction(1, 2)))
# R2 length check: 1/n^2 - 1/(n+1)^2 == (2n+1)/(n^2 (n+1)^2)
for n in range(1, 50):
    assert Fraction(1, n * n) - Fraction(1, (n + 1) ** 2) == Fraction(2 * n + 1, n * n * (n + 1) ** 2)
    assert Fraction(2 * n + 1, n * (n + 1) ** 2) <= Fraction(3, n * n)
print("L04 R2 identities ok")

# L01: brute force counts over all subfamilies, closure by enumeration
def gen(omega, blocks):
    fam = set()
    for mask in range(2 ** len(blocks)):
        u = frozenset().union(*[b for j, b in enumerate(blocks) if mask >> j & 1]) if mask else frozenset()
        fam.add(u)
    return fam
def closed(omega, fam):
    W = frozenset(omega)
    return (frozenset() in fam and W in fam, all(W - a in fam for a in fam), all((a | b) in fam for a in fam for b in fam))
print("L01", len(gen(range(4), [frozenset({0,1}), frozenset({2,3})])), closed(range(4), gen(range(4), [frozenset({0,1}), frozenset({2,3})])))
print("L01", len(gen(range(4), [frozenset({i}) for i in range(4)])))
print("L01", len(gen(range(6), [frozenset({0,1}), frozenset({2,3}), frozenset({4,5})])))
cand = {frozenset(), frozenset({0,1}), frozenset(range(4))}
print("L01 candidate", closed(range(4), cand))
# L01 M1 solution: blocks {1},{2,3},{4,5} on {1..5}
print("L01 M1 members", sorted(map(sorted, gen(range(1,6), [frozenset({1}), frozenset({2,3}), frozenset({4,5})])), key=lambda x:(len(x),x)))

# L02: exact counts
W6 = range(1, 7)
subsets = [frozenset(c) for r in range(7) for c in __import__("itertools").combinations(W6, r)]
print("L02 subsets", len(subsets))
disj = [(a, b) for a in subsets for b in subsets if not (a & b)]
fail = [(a, b) for (a, b) in disj if Fraction(len(a | b), 6) ** 2 != Fraction(len(a), 6) ** 2 + Fraction(len(b), 6) ** 2]
print("L02 disjoint pairs", len(disj), "failing", len(fail), "both nonempty", sum(1 for a, b in disj if a and b))
print("L02 3/20 total", 6 * Fraction(3, 20))
print("L02 prop 3.1 example", Fraction(2, 6) + Fraction(2, 6), Fraction(3, 6))
print("L02 biased odd", Fraction(1, 2) + Fraction(1, 8) + Fraction(1, 32))
print("L02 weights sum", sum([Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 16), Fraction(1, 32), Fraction(1, 32)]))
print("L02 E1 pairs 4pt", 3 ** 4, "6pt", 3 ** 6, "pairs with empty member", 64 + 64 - 1)

# L03 Part A
print("L03 A", Fraction(1, 2) * 0 + Fraction(1, 4) * 1 + Fraction(1, 4) * 3)
print("L03 M1", 2 * Fraction(1, 3) + 5 * Fraction(2, 3))
print("L03 M2", Fraction(1, 2) + Fraction(1, 4))
# L04 Lab A
print("L04 f_n(1/5)", [n if Fraction(1, 5) <= Fraction(1, n) else 0 for n in range(1, 9)])
