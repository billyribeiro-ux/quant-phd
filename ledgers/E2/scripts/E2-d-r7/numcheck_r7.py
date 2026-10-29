"""Round-7 re-derivation of the numbers in the E2 project slice and of the cards that quote them (verifier-authored)."""

from __future__ import annotations

import itertools
from fractions import Fraction
from math import floor

# E[M] for n = 5, a = 2000 (L08 Proposition 2.2 summed exactly); F(x) = (x + a + 1)/(2a + 1)
n, a = 5, 2000
F = lambda x: Fraction(x + a + 1, 2 * a + 1)  # noqa: E731
EM = -a + sum(1 - F(x) ** n for x in range(-a, a))
print("E[M] exact:", EM, "=", float(EM))
print("E[M] equals 85418692002000/64048012001:", EM == Fraction(85418692002000, 64048012001))
print("E[M] to 8 dp:", f"{float(EM):.8f}", " 1333.67 to 2 dp:", f"{float(EM):.2f}")
print("1333 - E[M] exact:", 1333 - EM, " rounded 2 dp:", f"{float(1333 - EM):.2f}")
print("1334 - E[M] exact:", 1334 - EM, "; smallest integer >= E[M]:", floor(EM) + (0 if EM == floor(EM) else 1))
print("20000 * E[M] rounded to cent:", round(20000 * EM), " (L08 Lab 1 Part B prints -26673331 for the total)")
print("continuous analogue a(n-1)/(n+1):", Fraction(a * (n - 1), n + 1), float(Fraction(a * (n - 1), n + 1)))
print("difference discrete - continuous:", float(EM - Fraction(4000, 3)))

# Project engine values (grader reference rules, re-derived here independently in integers)
def rank(bids):
    return sorted(range(len(bids)), key=lambda i: (-bids[i], i))

def pay(fmt, bids, k):
    r = rank(bids)
    win = set(r[:k])
    clear = bids[r[k]]
    return [(clear if fmt == "uniform" else bids[i]) if i in win else 0 for i in range(len(bids))]

# Lab 1 (project page): bids 5200, 4800, 6100, 3900, k = 2
b1 = [5200, 4800, 6100, 3900]
print("Lab1 uniform:", pay("uniform", b1, 2), sum(pay("uniform", b1, 2)), "disc:", pay("discriminatory", b1, 2), sum(pay("discriminatory", b1, 2)))
print("Lab1 gap share:", f"{100 * 1700 / 9600:.1f}")
# Lab 3 (project page): bids 7400 6200 8100 6200 5300, values 6000 7800 9000 6900 5000, k = 3
b3 = [7400, 6200, 8100, 6200, 5300]
v3 = [6000, 7800, 9000, 6900, 5000]
print("Lab3 ranking:", rank(b3), "uniform rev:", sum(pay("uniform", b3, 3)), "disc rev:", sum(pay("discriminatory", b3, 3)))
print("Lab3 gap share:", f"{100 * 3100 / 18600:.1f}")
won = sum(v3[i] for i in rank(b3)[:3])
best = sum(sorted(v3, reverse=True)[:3])
print("Lab3 won:", won, "best:", best, "share:", f"{100 * won / best:.1f}")
# symmetric bids at v = 7300 for n = 2..5 (closed form, half up)
for nn in range(2, 6):
    exact = Fraction((nn - 1) * 7300, nn)
    print("n", nn, "bid", floor(exact + Fraction(1, 2)), "exact", exact)
# Exemplar A revenue figures and efficiency share
print("exemplar A: 3100/18600 =", f"{100*3100/18600:.1f}", "; 22800/23700 =", f"{100*22800/23700:.1f}")

# L09 R1 / card c120: profiles over {0,1,2,3}^4 with k = 2 and equal revenues
cnt = 0
above = 0
for b in itertools.product(range(4), repeat=4):
    ru = sum(pay("uniform", list(b), 2))
    rd = sum(pay("discriminatory", list(b), 2))
    if rd == ru:
        cnt += 1
    elif rd > ru:
        above += 1
    else:
        raise SystemExit("discriminatory below uniform found")
print("k=2 equal:", cnt, "discriminatory above:", above, "total:", 4**4)
print("count formula 4w+1 summed over w=0..3:", sum(4 * w + 1 for w in range(4)))
# L09 Lab 1 Part C: k = 1 -> uniform charges b(2); discriminatory b(1)
ok = 0
for b in itertools.product(range(4), repeat=4):
    r = rank(list(b))
    u = pay("uniform", list(b), 1)
    d = pay("discriminatory", list(b), 1)
    if u[r[0]] == sorted(b, reverse=True)[1] and d[r[0]] == sorted(b, reverse=True)[0]:
        ok += 1
print("k=1 profiles agreeing with Prop 4.1 (over 4^4):", ok)
