"""Round-3: recompute every number that project.html states in Labs 1 and 3, the Lab 2 interpretation, and the two exemplars."""
from fractions import Fraction as F
import math


def rnd(x):
    return math.floor(x + F(1, 2))


def gap(c, p, s, k, df):
    return F(c) - F(p) - (F(s) - F(k) * F(df, 10**6))


def chord_minus_call(k, c, j):
    k0, k1, k2 = k[j - 1], k[j], k[j + 1]
    return F(k2 - k1, k2 - k0) * c[j - 1] + F(k1 - k0, k2 - k0) * c[j + 1] - c[j]


def lab(strikes, calls, puts, spot, df, fee, spread, name):
    cost = 3 * (fee + spread)
    print(f"-- {name}: cost per finding {cost}")
    for i, k in enumerate(strikes):
        g = gap(calls[i], puts[i], spot, k, df)
        gr = rnd(abs(g))
        print(f"   strike {k}: gap {rnd(g)} gross {gr} net {gr - cost}")
    for j in range(1, len(strikes) - 1):
        d = chord_minus_call(strikes, calls, j)
        print(f"   convex {strikes[j]}: chord-call {d}" + (f" gross {rnd(-d)} net {rnd(-d) - cost}" if d < 0 else ""))


lab([9000, 9500, 10000, 10500, 11000, 11500], [1500, 1100, 800, 700, 450, 350], [410, 385, 700, 1095, 1360, 1735],
    10000, 990000, 5, 10, "Lab 1 / Lab 2 chain")
lab([4000, 4500, 5000, 6000, 6500, 7000], [1210, 820, 500, 330, 151, 90], [10, 155, 250, 1030, 1100, 1200],
    5000, 950000, 8, 12, "Lab 3 chain")
print("-- exemplar B: discounted strikes", F(6500 * 950000, 10**6), F(7000 * 950000, 10**6))
print("   chord at 6000 =", F(500, 3) + F(2 * 151, 3), "(= 802/3); call 330; chord-call =", F(802, 3) - 330)
print("   parity gap 6500 =", gap(151, 1100, 5000, 6500, 950000), "; 7000 =", gap(90, 1200, 5000, 7000, 950000))
