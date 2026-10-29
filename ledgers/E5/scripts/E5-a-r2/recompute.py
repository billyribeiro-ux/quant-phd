"""Round 2 independent recomputation for E5 slice a (index, L01-L03). Run as: python -I recompute.py"""
import math
from decimal import Decimal, getcontext
from fractions import Fraction as F

getcontext().prec = 60
# L01 numbers
print("L01 ln1.25", round(math.log(1.25), 6), "ln1.1-0.1", round(math.log(1.1) - 0.1, 6), "1.1-1 simple", round(1.1 - 1, 6))
print("L01 0.25-ln1.25", round(0.25 - math.log(1.25), 6), "7/92", float(F(7, 92)), "105/995", float(F(105, 995)), "4/23", float(F(4, 23)))
g_r = F(25300, 27) / 995 - 1
print("L01 real growth exact", g_r, float(g_r), "check (1+gr)(1+pi)==1100/995:", (1 + g_r) * (1 + F(4, 23)) == F(1100, 995))
print("L01 rung-1 Laspeyres", F(2 * 1 + 2 * 1, 1 * 1 + 2 * 1), "M2", F(2 * 6 + 3 * 2, 1 * 6 + 4 * 2), float(F(9, 7)))
print("L01 E2 11/10-19/10", F(11, 10) - F(19, 10))
# L02 numbers: rebuild the seeded economy exactly as in the twin
import random
ALPHA, H, SEED = 0.3, 40, 2026
rng = random.Random(SEED)
A, K, L = [1.0], [100.0], [50.0]
for _ in range(H):
    A.append(A[-1] * math.exp(rng.uniform(0.005, 0.02)))
    K.append(K[-1] * math.exp(rng.uniform(0.02, 0.05)))
    L.append(L[-1] * math.exp(rng.uniform(0.0, 0.015)))
Y = [a * k ** ALPHA * l ** (1 - ALPHA) for a, k, l in zip(A, K, L)]
dY = [math.log(Y[t]) - math.log(Y[t - 1]) for t in range(1, H + 1)]
dK = [math.log(K[t]) - math.log(K[t - 1]) for t in range(1, H + 1)]
dL = [math.log(L[t]) - math.log(L[t - 1]) for t in range(1, H + 1)]
dA = [math.log(A[t]) - math.log(A[t - 1]) for t in range(1, H + 1)]
res = [y - ALPHA * k - (1 - ALPHA) * l for y, k, l in zip(dY, dK, dL)]
mean = lambda v: sum(v) / len(v)
print("L02 max|res-dlnA|", max(abs(r - a) for r, a in zip(res, dA)))
mY, mK, mL = mean(dY), mean(dK), mean(dL)
print("L02 means", round(mY, 6), round(mK * ALPHA, 6), round((1 - ALPHA) * mL, 6), round(mean(res), 6))
print("L02 shares", round(ALPHA * mK / mY, 6), round((1 - ALPHA) * mL / mY, 6), round(mean(res) / mY, 6))
r02 = mean([y - 0.2 * k - 0.8 * l for y, k, l in zip(dY, dK, dL)])
r04 = mean([y - 0.4 * k - 0.6 * l for y, k, l in zip(dY, dK, dL)])
print("L02 alt residuals", round(r02, 6), round(r04, 6), "diff", round(r02 - r04, 6), "0.2*(mK-mL)", round(0.2 * (mK - mL), 6))
print("L02 E2 implied avg dlnK", round(0.010667 / 0.3, 6), "avg dlnL", round(0.005327 / 0.7, 6), "0.2*(diff)", round(0.2 * (0.010667 / 0.3 - 0.005327 / 0.7), 6))
print("L02 E3 0.4*avgK", round(0.4 * 0.010667 / 0.3, 6))
print("L02 MisC3 1.1^0.3", round(1.1 ** 0.3, 6), "simple", round(1.1 ** 0.3 - 1, 6), "0.3ln1.1", round(0.3 * math.log(1.1), 6))
print("L02 M2 0.3 ln2", round(0.3 * math.log(2), 6), "M3", 0.04 - 0.25 * 0.05 - 0.75 * 0.02, "R3", 0.01 - 0.3 * 0.05)
print("L02 check", all(math.log(1 + s) <= s for s in [y / x - 1 for x, y in zip(Y[:-1], Y[1:])]), round(mean([y / x - 1 for x, y in zip(Y[:-1], Y[1:])]), 6))
# L03 numbers, exact decimal
al, s, d, n, k0 = Decimal("0.3"), Decimal("0.2"), Decimal("0.05"), Decimal("0.01"), Decimal(1)
kstar = (s / (n + d)) ** (1 / (1 - al))
print("L03 k*", f"{kstar:.10f}", "y*", f"{kstar ** al:.10f}")
g = lambda k: (s * k ** al + (1 - d) * k) / (1 + n)
print("L03 dk/ds", f"{kstar / ((1 - al) * s):.10f}", "dk/ddelta", f"{-kstar / ((1 - al) * (n + d)):.10f}")
print("L03 E1 ratio", Decimal("0.0805861272") / Decimal("0.6623874908"))
print("L03 E2 pct", Decimal("0.01") * kstar / ((1 - al) * s) / kstar, "elasticity", 1 / (1 - al))
print("L03 E3 linear", Decimal("0.001") * (-kstar / ((1 - al) * (n + d))))
k = k0; first = None
for t in range(1, 1001):
    k = g(k)
    if first is None and abs(k - kstar) < Decimal("1e-12"):
        first = t
print("L03 first period <1e-12", first)
cnt_below = sum(1 for i in range(1, 51) if Decimal(i) / 5 < kstar)
print("L03 grid below/above", cnt_below, 50 - cnt_below)
k2 = (Decimal("0.25") * Decimal("1.15").sqrt() + Decimal("0.9") * Decimal("1.15"))
print("M2 k2", f"{k2:.10f}", "sqrt1.15", f"{Decimal('1.15').sqrt():.10f}")
