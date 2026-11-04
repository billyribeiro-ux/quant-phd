"""Independent recomputation of the L03 and L04 numbers (LX1 slice b, round 1). Uses Fraction and decimal only."""
import csv
import math
import sys
from decimal import Decimal, getcontext, ROUND_HALF_UP
from fractions import Fraction

getcontext().prec = 50
root = sys.argv[1]

def q(x, places):
    return Decimal(x).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)

# ---------- L03 ----------
D = Fraction(1_000_000); N0 = Fraction(4_000_000); delta = Fraction(1, 50); H = 12
def P(m, t): return (1 - delta) ** min(t, m)
def V(m, t): return D / P(m, t)
def lev(v): return v / (N0 + D - v)
L0 = lev(D)
def depth_exact(m, phi=Fraction(1), beta=Fraction(1)):
    return max(beta * phi * (lev(V(m, t)) - L0) for t in range(H + 1))
dX = depth_exact(12); dY = depth_exact(4)
print("L03 depth X exact (percent):", q(Decimal(100 * dX.numerator) / Decimal(dX.denominator), 6))
print("L03 depth Y exact (percent):", q(Decimal(100 * dY.numerator) / Decimal(dY.denominator), 6))
print("L03 depth X printed-2dp:", q(Decimal(100 * dX.numerator) / Decimal(dX.denominator), 2))
print("L03 depth Y printed-2dp:", q(Decimal(100 * dY.numerator) / Decimal(dY.denominator), 2))
diff = 100 * (dX - dY)
print("L03 X minus Y exact (pp):", q(Decimal(diff.numerator) / Decimal(diff.denominator), 6), "rounded 2dp", q(Decimal(diff.numerator)/Decimal(diff.denominator), 2))
print("L03 2dp difference of printed values:", Decimal("9.20") - Decimal("2.69"))
ratio = dX / dY
print("L03 ratio X/Y exact:", q(Decimal(ratio.numerator) / Decimal(ratio.denominator), 8), "4dp", q(Decimal(ratio.numerator) / Decimal(ratio.denominator), 4))
for phi, beta in [(Fraction(1, 2), Fraction(1)), (Fraction(3), Fraction(1))]:
    r = depth_exact(12, phi, beta) / depth_exact(4, phi, beta)
    print("L03 ratio at phi,beta", phi, beta, "=", q(Decimal(r.numerator) / Decimal(r.denominator), 10))
V12 = V(12, 12); V4 = V(4, 4)
print("L03 V_12 exact cents:", q(Decimal(V12.numerator) / Decimal(V12.denominator), 4))
print("L03 V_4 exact cents:", q(Decimal(V4.numerator) / Decimal(V4.denominator), 4))
print("L03 P_4 exact:", P(4, 4), "=", float(P(4, 4)))
N4 = N0 - (V4 - D)
print("L03 N_4 exact:", q(Decimal(N4.numerator) / Decimal(N4.denominator), 4))
L4 = V4 / N4
print("L03 L_4 exact:", q(Decimal(L4.numerator) / Decimal(L4.denominator), 7))
print("L03 psi at t=4 Y exact:", q(Decimal((lev(V4) - L0).numerator) / Decimal((lev(V4) - L0).denominator), 6))
# Y depth first attained at t=4 and flat after
print("L03 Y path: V_t for t>=4 equals V_4:", all(V(4, t) == V4 for t in range(4, 13)))
# unchanged-index count for Y
idx = [P(4, t) for t in range(13)]
print("L03 Y index unchanged periods (t=1..12):", sum(1 for t in range(1, 13) if idx[t] == idx[t - 1]))
# Part C monotone check exact
dep = [depth_exact(m) for m in range(13)]
print("L03 Part C never falls:", all(dep[m] <= dep[m + 1] for m in range(12)), "strict:", all(dep[m] < dep[m + 1] for m in range(12)))
# hypothesis: V_m reached earliest at t=m
print("L03 X real debt 12 rounds:", q(Decimal(V12.numerator) / Decimal(V12.denominator), 0))

# ---------- L04 ----------
rows = []
with open(f"{root}/course/assets/data/market/fx_monthly.csv", encoding="utf-8", newline="") as h:
    rd = csv.DictReader(h)
    fields = rd.fieldnames
    for r in rd:
        rows.append((r["month"], r["GBP"]))
print("L04 fieldnames:", fields)
print("L04 rows:", len(rows), rows[0][0], rows[-1][0])
blank = [m for m, v in rows if v.strip() == ""]
print("L04 GBP blanks:", len(blank))
bad = [(m, v) for m, v in rows if not v.replace(".", "", 1).isdigit()]
print("L04 GBP non-decimal cells:", bad[:5], len(bad))
rates = [(m, Decimal(v)) for m, v in rows]
# log changes via high precision decimal ln
def ln(x): return x.ln()
changes = [(rates[i][0], ln(rates[i][1] / rates[i - 1][1])) for i in range(1, len(rates))]
zeros = [m for i, (m, c) in enumerate(changes) if rates[i + 1][1] == rates[i][1]]
print("L04 zero changes:", len(zeros), zeros)
def sd(vals):
    n = len(vals); mu = sum(vals) / n
    return (sum((v - mu) ** 2 for v in vals) / (n - 1)).sqrt()
w1 = [c for _, c in changes]
w2_idx = [i for i, (m, _) in enumerate(changes) if m >= "2000-01"]
w2 = [changes[i][1] for i in w2_idx]
s1 = sd(w1); s2 = sd(w2)
print("L04 n1", len(w1), "n2", len(w2), "first w2 month", changes[w2_idx[0]][0], "last", changes[-1][0])
print("L04 sd1 =", q(s1, 6), "sd2 =", q(s2, 6))
print("L04 sd2 - sd1 exact-based (6dp):", q(s2 - s1, 6), " from displayed digits:", Decimal("0.024700") - Decimal("0.027935"))
print("L04 ratio s2/s1 (4dp):", q(s2 / s1, 4))
mx1 = max(changes, key=lambda it: abs(it[1]))
mx2 = max([changes[i] for i in w2_idx], key=lambda it: abs(it[1]))
print("L04 largest w1:", mx1[0], q(mx1[1], 6), "largest w2:", mx2[0], q(mx2[1], 6))
print("L04 unrounded largest w1 abs:", mx1[1], "w2 signed:", mx2[1])
# simple change for 2008-10
L = mx2[1]
print("L04 E2 simple change e^L - 1 (6dp):", q((L.exp() - 1), 6))
# R2 band
Lw1 = abs(mx1[1])
h = ((Lw1.exp() - 1) / (Lw1.exp() + 1))
print("L04 R2 h exact:", q(h, 7))
print("L04 bound at h=0.0678:", q(((Decimal("1.0678")) / (Decimal("0.9322"))).ln(), 6), q(((Decimal("1.0678")) / (Decimal("0.9322"))).ln(), 4))
print("L04 bound at h=0.0678 full:", ((Decimal("1.0678")) / (Decimal("0.9322"))).ln())
print("L04 log 1.1:", q(Decimal("1.1").ln(), 10), "diff from 0.1:", q(Decimal("0.1") - Decimal("1.1").ln(), 7))
print("L04 window two changes 2000-01..2026-09:", sum(1 for m, _ in changes if m >= "2000-01"))
print("L04 sample checks: 1999-12 rate", dict(rates).get("1999-12"), "2000-01 rate", dict(rates).get("2000-01"))
