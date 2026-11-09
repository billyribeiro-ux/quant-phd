"""Independent re-derivation (own code, no lab imports) of the numbers quoted in the quiz explanations and the
delta-changed prose of L01, L03 and L04. Run as: python -I quiz_numbers_r23.py <checkout_root>."""
import csv
import math
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F

ROOT = sys.argv[1]


def rhu(x, places=0):
    q = Decimal(1).scaleb(-places)
    return Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP) if isinstance(x, float) else Decimal(x.numerator) / Decimal(x.denominator) if False else None


def half_up(fr, places):
    scaled = fr * 10**places
    return math.floor(scaled + F(1, 2)) / 10**places


print("== L01 quiz 6 (Proposition 1.4) checks")
d1, r, g = F(400), F(9, 100), F(1, 100)
for gg in [F(9, 100), F(10, 100), F(3, 100)]:
    if gg >= r:
        q = (1 + gg) / (1 + r)
        print("g", gg, "q", q, "q>=1", q >= 1, "term1", d1 * q**0 / (1 + r), "terms >= d1/(1+r):", all(d1 * q**(k - 1) / (1 + r) >= d1 / (1 + r) for k in range(1, 200)))
# partial sums for g = 10%, r = 9%, to show growth without bound
S = F(0)
for k in range(1, 201):
    S += (F(400) * (1 + F(10, 100)) ** (k - 1)) / (1 + r) ** k
print("S_200 at g=10%, r=9% (float)", float(S))
print("quiz 1: F0 =", F(400) / F(6, 100), "=", float(F(400) / F(6, 100)), "half-up 0dp", half_up(F(400) / F(6, 100), 0))
print("quiz 2: F2 =", F(400) * F(103, 100) ** 2 / F(6, 100), float(F(400) * F(103, 100) ** 2 / F(6, 100)), "-> 2dp", half_up(F(400) * F(103, 100) ** 2 / F(6, 100), 2))
print("quiz 3: q", F(103, 109), float(F(103, 109)))
print("quiz 4: g* =", F(9, 100) - F(400, 6000), float(F(9, 100) - F(400, 6000)))
print("witness: F0(1%)", F(400) / (F(9, 100) - F(1, 100)), "F0(3%)", F(400) / (F(9, 100) - F(3, 100)), "gap 6000:", F(6000) - F(400) / (F(9, 100) - F(1, 100)), float(F(6000) - F(400) / (F(9, 100) - F(3, 100))))
print("quiz 7: Y 400 cents, r=9% closed-form at g=3% (misconception 2)", F(400) / (F(9, 100) - F(3, 100)), "  present value of 400 alone", F(400) / F(109, 100), "=", float(F(400) / F(109, 100)))
print("misc3: g=10%, r=9% closed form", F(400) / (F(9, 100) - F(10, 100)), float(F(400) / (F(9, 100) - F(10, 100))))

print("== L03 numbers (own model)")
DEBT = F(1_000_000)
K0 = F(4_000_000)
DELTA = F(1, 50)
H = 12
PHI = F(1)
BETA = F(1)


def path(m):
    out = []
    for t in range(H + 1):
        P = (1 - DELTA) ** min(t, m)
        V = DEBT / P
        K = K0 - (V - DEBT)
        L = V / K
        L0 = DEBT / K0
        out.append((t, P, V, K, L, BETA * PHI * (L - L0)))
    return out


def depth(m):
    p = path(m)
    mx = max(x[5] for x in p)
    t_first = next(x[0] for x in p if x[5] == mx)
    return mx, t_first


dX, tX = depth(12)
dY, tY = depth(4)
print("depth X", float(dX), "first t", tX, "2dp", half_up(dX, 2))
print("depth Y", float(dY), "first t", tY, "2dp", half_up(dY, 2), "exact", dY)
print("ratio X/Y", float(dX / dY), "4dp", half_up(dX / dY, 4))
print("diff X-Y 2dp", half_up(dX - dY, 2), float(dX - dY))
print("V_12 for X", float(path(12)[12][2]), "exact", path(12)[12][2], "rounded to cents", math.floor(path(12)[12][2] + F(1, 2)))
print("Y price index flat t>=4 periods unchanged from prior: count of t in 1..12 with P_t == P_{t-1}:", sum(1 for t in range(1, 13) if path(4)[t][1] == path(4)[t - 1][1]), "t list", [t for t in range(1, 13) if path(4)[t][1] == path(4)[t - 1][1]])
print("Y depth at t=4 (= first max):", float(path(4)[4][5]))
print("X depth path (2dp):", [str(half_up(x[5], 2)) for x in path(12)])
print("Y depth path (2dp):", [str(half_up(x[5], 2)) for x in path(4)])
print("ratio depth for beta*phi=1/2, 3 (should be equal):", [float((dX * b) / (dY * b)) for b in [F(1, 2), F(3)]])
print("Part C depths 2dp:", [str(half_up(depth(m)[0], 2)) for m in range(13)])
print("L03 quiz 'X depth first reached at t = 12': first t =", tX)

print("== L04 numbers (own code, from the embedded CSV)")
rows = list(csv.DictReader(open(f"{ROOT}/course/assets/data/market/fx_monthly.csv", encoding="utf-8")))
months = [r_["month"] for r_ in rows]
gbp = [F(r_["GBP"]) for r_ in rows]
print("rows", len(rows), months[0], months[-1])
ch = {}
for i in range(1, len(rows)):
    ch[months[i]] = math.log(float(gbp[i]) / float(gbp[i - 1])) if False else None
# high-precision logs via Decimal
from decimal import getcontext
getcontext().prec = 50


def dln(x):
    return Decimal(x.numerator) / Decimal(x.denominator)


ells = {}
for i in range(1, len(rows)):
    ratio = dln(gbp[i]) / dln(gbp[i - 1])
    ells[months[i]] = ratio.ln()
w1 = [(m_, ells[m_]) for m_ in months[1:]]
w2 = [(m_, ells[m_]) for m_ in months[1:] if m_ >= "2000-01"]
print("window one n", len(w1), "window two n", len(w2), "w2 first", w2[0][0])


def sd(vals):
    n = len(vals)
    mean = sum(vals) / n
    return (sum((v - mean) ** 2 for v in vals) / (n - 1)).sqrt()


s1 = sd([v for _, v in w1])
s2 = sd([v for _, v in w2])
print("s1 6dp", half_up(F(str(s1)), 6), "s2 6dp", half_up(F(str(s2)), 6), "diff", s2 - s1)
print("ratio s2/s1 4dp", half_up(F(str(s2 / s1)), 4))
zeros = [m_ for m_, v in w1 if v == 0]
print("zero changes in window one", zeros, len(zeros), "nonzero", len(w1) - len(zeros))
mx1 = max(w1, key=lambda t: abs(t[1]))
mx2 = max(w2, key=lambda t: abs(t[1]))
print("largest abs w1", mx1[0], float(abs(mx1[1])), "w2", mx2[0], float(mx2[1]))
print("ln(1.1)", Decimal("1.1").ln())
h = F("0.0678")
print("bound at h=0.0678: ln((1+h)/(1-h))", float((dln(1 + h) / dln(1 - h)).ln()) if False else float((Decimal(1 + h.numerator * 1) / 1).ln()) if False else None)
bound = (Decimal(1) + Decimal("0.0678")).ln() - (Decimal(1) - Decimal("0.0678")).ln()
print("bound ln(1.0678)-ln(0.9322) =", bound, "4dp", bound.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))
print("telescoping check window one: sum ells - ln(x_b/x_a)")
tot = sum(ells[m_] for m_ in months[1:])
print("max diff", float(abs(tot - (dln(gbp[-1]) / dln(gbp[0])).ln())))
