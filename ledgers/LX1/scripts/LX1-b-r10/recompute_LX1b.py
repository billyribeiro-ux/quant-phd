"""Independent recomputation of every number in LX1 L03 and L04 prose (exact Fractions, own code, not the twins).

Usage: python3 -I recompute_LX1b.py <checkout>
"""
import csv
import math
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
from pathlib import Path

root = Path(sys.argv[1])


def r(x, places):
    q = Decimal(1).scaleb(-places)
    return Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP) if not isinstance(x, F) else \
        (Decimal(x.numerator) / Decimal(x.denominator)).quantize(q, rounding=ROUND_HALF_UP)


print("== L03 model (exact Fractions) ==")
D, N0, delta, H, mX, mY = F(1_000_000), F(4_000_000), F(1, 50), 12, 12, 4
phi = beta = F(1)


def P(m, t):
    return (1 - delta) ** min(t, m)


def V(m, t):
    return D / P(m, t)


def Lev(v):
    return v / (N0 + D - v)


L0 = Lev(D)
print("L0 exact", L0, "=", float(L0))


def psi(m, t, ph=phi):
    return ph * (Lev(V(m, t)) - L0)


def f(m, t, b=beta, ph=phi):
    return b * psi(m, t, ph)


def depth(m, b=beta, ph=phi):
    return max(f(m, t, b, ph) for t in range(H + 1))


def first_t(m):
    top = depth(m)
    return next(t for t in range(H + 1) if f(m, t) == top)


for name, m in (("X", mX), ("Y", mY)):
    print(f"economy {name}: depth exact {float(depth(m))*100:.6f}% first t={first_t(m)}")
    for t in range(H + 1):
        p = P(m, t)
        v = V(m, t)
        print(f"  t={t:2d} P={r(p,4)} V={r(v,4)} rounded cents={int(math.floor(v + F(1,2)))} L={r(Lev(v),4)} psi={r(psi(m,t),4)} fall%={r(100*f(m,t),2)}")
dX, dY = depth(mX), depth(mY)
print("X-Y exact % =", float(100 * (dX - dY)), "rounded", r(100 * (dX - dY), 2), "difference of printed", F(920, 100) - F(269, 100))
print("ratio X/Y exact =", float(dX / dY), "rounded4", r(dX / dY, 4))
for pr in (F(1, 2), F(1), F(3)):
    print("  ratio at phi=", pr, "=", r(depth(mX, F(1), pr) / depth(mY, F(1), pr), 6))
print("closed-form check Prop 3.2(b) X:", float(beta * phi * (Lev(V(mX, H)) - L0)))
print("V_12 exact float", float(V(mX, 12)), "rounded half up", int(math.floor(V(mX, 12) + F(1, 2))))
print("V_m < N0 + D:", V(mX, mX) < N0 + D, float(V(mX, mX)))
print("M1 P4 exact", P(4, 4), "=", float(P(4, 4)), " V4 =", float(V(4, 4)), " half-up cents", int(math.floor(V(4, 4) + F(1, 2))))
N4 = N0 - (V(4, 4) - D)
print("M2 N4 exact =", float(N4), " rounded", int(math.floor(N4 + F(1, 2))), " from rounded V4", int(N0 - F(1084166) + 0) - 0)
print("M3 L4 =", float(V(4, 4) / N4), r(V(4, 4) / N4, 4))
# E3: Y index unchanged periods t=1..12
unch = sum(1 for t in range(1, H + 1) if P(4, t) == P(4, t - 1))
print("E3 unchanged periods (Y):", unch)
# L03 misc: premium square variant ratio
print("ratio of Cor 3.4 =", float(depth(mX)/depth(mY)), " squared =", float((depth(mX)/depth(mY))**2))

print("\n== L04 data (floats per twin convention, decimal ratios) ==")
rows = []
with (root / "course/assets/data/market/fx_monthly.csv").open(encoding="utf-8", newline="") as h:
    rd = csv.DictReader(h)
    for rec in rd:
        rows.append((rec["month"], rec["GBP"]))
print("rows", len(rows), rows[0], rows[-1])
blank = [m for m, v in rows if v.strip() == ""]
print("GBP blank cells:", len(blank))
ex = [(m, F(v)) for m, v in rows]
changes = []
for (m0, a), (m1, b) in zip(ex, ex[1:]):
    changes.append((m1, math.log(float(b / a)), b == a))
zeros = [m for m, _, z in changes if z]
print("window one changes", len(changes), "zeros", zeros)


def sd(vals):
    n = len(vals)
    mu = math.fsum(vals) / n
    return math.sqrt(math.fsum((x - mu) ** 2 for x in vals) / (n - 1))


w1 = [c for _, c, _ in changes]
w2 = [c for m, c, _ in changes if m >= "2000-01"]
s1, s2 = sd(w1), sd(w2)
print("n1", len(w1), "sd1", repr(s1), "n2", len(w2), "sd2", repr(s2))
print("sd1 rounded", r(s1, 6), "sd2 rounded", r(s2, 6), "diff unrounded", s2 - s1, "rounded", r(s2 - s1, 6), "diff printed", F("0.024700") - F("0.027935"))
print("ratio", s2 / s1, "rounded4", r(s2 / s1, 4))
big1 = max(changes[:], key=lambda c: abs(c[1]))
print("largest window one", big1[0], big1[1], r(big1[1], 6))
w2c = [c for c in changes if c[0] >= "2000-01"]
big2 = max(w2c, key=lambda c: abs(c[1]))
print("largest window two", big2[0], big2[1], r(big2[1], 6), "simple change exp(L)-1 =", math.exp(big2[1]) - 1, r(math.exp(big2[1]) - 1, 6))
print("zero-change months window one count", len(zeros), "nonzero", len(changes) - len(zeros))
# window two start rate and sum identity
print("window two sum identity:", abs(math.fsum(w2) - math.log(float(ex[-1][1] / F(rows and dict(ex)['1999-12'])))))

print("\n== L04 problems ==")
print("M1 ln1.1 =", math.log(1.1), "difference", 0.1 - math.log(1.1))
print("M2 mean", F(2, 100) / 3, "sum sq dev", F(14, 10000) - 3 * F(1, 150) ** 2, "=", F(19, 15000), "dispersion", math.sqrt(19 / 30000))
L = 0.135846
h = math.tanh(L / 2)
print("R2 h exact-ish", h, "h rounded6", round(h, 6), "tanh(L/2) check (e^L-1)/(e^L+1)", (math.exp(L) - 1) / (math.exp(L) + 1))
print("bound at h=0.0678:", math.log(1.0678 / 0.9322), "bound at h=h*", math.log((1 + h) / (1 - h)))
print("ln(1.0678/0.9322)", math.log(F(10678, 10000) / F(9322, 10000)))
print("P2 bound ln((1+h)/(1-h)) form ok")
