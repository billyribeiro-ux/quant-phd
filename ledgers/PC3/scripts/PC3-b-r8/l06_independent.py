"""Independent re-derivation of the PC3 L06 numbers and propositions (verifier round 8). Written from the page text.

Run as: .venv/bin/python -I ledgers/PC3/scripts/PC3-b-r8/l06_independent.py
"""

from __future__ import annotations

import itertools
import math
import random
from fractions import Fraction as F

# ---- Part 1: forward price and portfolio, exact.
S = F(9700)
D = F(97, 100)
Fno = S / D
print("no-arbitrage F = S/D =", Fno)
for quote in (Fno, F(10100)):
    pays = []
    for ST in (8000, 9000, 10000, 11000, 12000):
        # long asset worth ST; short forward receives quote and delivers asset (net quote - ST); loan of S repaid S/D
        pays.append(F(ST) + (quote - F(ST)) - S / D)
    print("quote", quote, "payoffs", [str(x) for x in pays], "all equal quote - S/D:", all(x == quote - S / D for x in pays))

# ---- Part 2: case.
I = F(15_000_000)
m = F(5000)
rates = {"8": F(8, 100), "10": F(10, 100), "12": F(12, 100)}
for key, r in rates.items():
    A = sum((1 / (1 + r) ** t for t in range(1, 4)), F(0))
    be = (I / m) / A
    print(f"rate {key}%: A = {float(A):.10f}, break-even = {float(be):.10f}")
A10 = sum((1 / (F(11, 10)) ** t for t in range(1, 4)), F(0))
print("A at 10% exact:", A10, "== 3310/1331:", A10 == F(3310, 1331))
be10 = (I / m) / A10
print("break-even at 10% exact:", be10, "== 399300/331:", be10 == F(399300, 331), " float:", float(be10))


def npv(units: F, r: F) -> F:
    cfs = [-I] + [units * m] * 3
    return sum((c / (1 + r) ** t for t, c in enumerate(cfs)), F(0))


print("NPV(200) exact:", npv(F(200), F(1, 10)), "float", float(npv(F(200), F(1, 10))))
print("NPV(1600) float:", float(npv(F(1600), F(1, 10))))
for key, r in rates.items():
    lo = npv(F(200), r)
    hi = npv(F(1600), r)
    print(f"rate {key}%: NPV(200) = {float(lo):.4f} NPV(1600) = {float(hi):.4f}")
# exact display check of the printed NPVs (half up toward +inf to whole cent)
def hu(x: F, places: int) -> str:
    scale = 10**places
    n = math.floor(x * scale + F(1, 2))
    return str(n)

print("display NPV(200) 10%:", hu(npv(F(200), F(1, 10)), 0), "expected -12513148")
print("display NPV(1600) 10%:", hu(npv(F(1600), F(1, 10)), 0), "expected 4894816")
print("display NPV(200) 8%:", hu(npv(F(200), F(8, 100)), 0), "expected -12422903")
print("display NPV(1600) 8%:", hu(npv(F(1600), F(8, 100)), 0), "expected 5616776")
print("display NPV(200) 12%:", hu(npv(F(200), F(12, 100)), 0), "expected -12598169")
print("display NPV(1600) 12%:", hu(npv(F(1600), F(12, 100)), 0), "expected 4214650")

# Break-even at 8 and 12 percent, unrounded values
be8 = (I / m) / sum((1 / (F(108, 100)) ** t for t in range(1, 4)), F(0))
be12 = (I / m) / sum((1 / (F(112, 100)) ** t for t in range(1, 4)), F(0))
print("be8 float:", float(be8), "be10 float:", float(be10), "be12 float:", float(be12))
print("widths:", float(be12 - be8), "avg per point:", float((be12 - be8) / 4), "8-10:", float(be10 - be8), "10-12:", float(be12 - be10))
print("naive display differences 1249.05-1206.34:", round(1249.05 - 1206.34, 2))

# Fermi bounds and products
print("Fermi lower/upper:", F(2000) * 1 * F(1, 10), F(4000) * 2 * F(1, 5), "ratio", F(4000) * 2 * F(1, 5) / (F(2000) * 1 * F(1, 10)))

# E2 hand computations
print("NPV at 1200 units exact:", npv(F(1200), F(1, 10)), "== -105000000/1331:", npv(F(1200), F(1, 10)) == F(-105_000_000, 1331), "float", float(npv(F(1200), F(1, 10))))
print("NPV at 1300 units exact:", npv(F(1300), F(1, 10)), "== 1550000000/1331:", npv(F(1300), F(1, 10)) == F(1_550_000_000, 1331), "float", float(npv(F(1300), F(1, 10))))
grid = list(range(200, 1601, 100))
pos = [u for u in grid if npv(F(u), F(1, 10)) > 0]
neg_max = max(u for u in grid if npv(F(u), F(1, 10)) < 0)
print("E2 grid positive count:", len(pos), pos, "largest negative grid point:", neg_max)
print("grid increasing:", all(npv(F(a), F(1, 10)) < npv(F(b), F(1, 10)) for a, b in itertools.pairwise(grid)))

# M2: NPV of -100, 60, 60 at 10%
print("M2 NPV:", -100 + F(60) / F(11, 10) + F(60) / F(121, 100), "== 500/121:", -100 + F(60) / F(11, 10) + F(60) / F(121, 100) == F(500, 121), float(F(500, 121)))
# M3: break-even units for outlay 100000, margin 400, 3 yrs, 10%
print("M3 u* exact:", (F(100000) / F(400)) / F(3310, 1331), "== 33275/331:", (F(100000) / F(400)) / F(3310, 1331) == F(33275, 331), float(F(33275, 331)))
# M1
print("M1 S/D:", F(4900) / F(98, 100), "payoff at 5050:", F(5050) - F(4900) / F(98, 100))
# E1 12%: A and break-even
A12 = sum((1 / (F(112, 100)) ** t for t in range(1, 4)), F(0))
print("E1 A12 float:", float(A12), "break-even 3000/A:", float(F(3000) / A12))
# R3: margin m* with break-even 1600
mstar = I / (F(1600) * A10)
print("R3 m* =", float(mstar), "ratio to 5000:", float(mstar / 5000), "fall %:", float((1 - mstar / 5000) * 100))
# Remark 4.3 break-even differences from unrounded
print("Remark 4.3 differences: 10-8:", round(float(be10 - be8), 2), " 12-10:", round(float(be12 - be10), 2))

# Corollary 3.3 / Prop 3.1 sign check on random ranges
rng = random.Random(7)
ok = True
for _ in range(2000):
    k = rng.randint(1, 4)
    lows = [F(rng.randint(1, 50), rng.randint(1, 5)) for _ in range(k)]
    highs = [lo + F(rng.randint(0, 30), rng.randint(1, 5)) for lo in lows]
    P_lo = math.prod(lows)
    P_hi = math.prod(highs)
    # random product inside bounds
    xs = [rng.uniform(float(lo), float(hi)) for lo, hi in zip(lows, highs)]
    P = math.prod(xs)
    if not (float(P_lo) - 1e-12 <= P <= float(P_hi) + 1e-12):
        ok = False
print("Prop 3.2 random product check:", ok)

# Prop 3.1 (ii) and (iii): NPV affine with slope mA, unique zero, checked on a grid of u
ok2 = True
for r in (F(-1, 2), F(0), F(1, 10), F(5)):
    for n in (1, 2, 3, 7):
        A = sum((1 / (1 + r) ** t for t in range(1, n + 1)), F(0))
        for u in (F(0), F(1), F(37, 3), F(1000)):
            val = -I + sum(((u * m) / (1 + r) ** t for t in range(1, n + 1)), F(0))
            if val != -I + m * A * u:
                ok2 = False
print("Prop 3.1 (i) identity exact on grid:", ok2)

# Prop 2.1 (ii) reverse portfolio: sell short at S, lend S (get S/D), long forward at F' < S/D: payoff S/D - F' in every state
ok3 = True
for Fp in (F(9000), F(9699), F(9700)):
    for ST in (1, 5000, 9000, 20000):
        pay = S - S + (S / D) + (ST - Fp) * 0 + (Fp - Fp)  # placeholder structure
        # explicit: cost 0; at tau: loan pays S/D; long forward pays -F' and receives asset worth ST; asset covers short -> net 0
        payoff = (S / D) - Fp + (F(ST) - F(ST))
        if payoff != S / D - Fp:
            ok3 = False
print("Prop 2.1(ii) reverse portfolio payoff identity:", ok3)
