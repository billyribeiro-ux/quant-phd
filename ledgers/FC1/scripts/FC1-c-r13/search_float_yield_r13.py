"""Round-13: find a valid (yield_bps, one-event amount) where the exact present value is a half cent and the float-rate
mutant r13n03 (Fraction(rate / 10000)) rounds it the other way. Prints the first hits."""
import math
from fractions import Fraction as F


def half_away(x):
    m = abs(x)
    r = math.floor(m + F(1, 2))
    return r if x >= 0 else -r


hits = []
for bps in range(1, 3000):
    y = F(bps, 10_000)
    yf = F(bps / 10_000)
    if yf == y:
        continue
    d = 10_000 + bps
    # exact PV of one event A at period 1 is A / (1 + y) = A * 10000 / d. Need it to be m + 1/2: 20000 A / d odd integer.
    for A in range(1, 400_000):
        pv = F(A) / (1 + y)
        if pv.denominator != 2:
            continue
        exact = half_away(pv)
        flt = half_away(F(A) / (1 + yf))
        if exact != flt:
            hits.append((bps, A, str(pv), exact, flt))
            break
    if len(hits) >= 5:
        break
for h in hits:
    print("yield_bps", h[0], "amount", h[1], "exact PV", h[2], "reference", h[3], "float-rate mutant", h[4])
print("hits", len(hits))
