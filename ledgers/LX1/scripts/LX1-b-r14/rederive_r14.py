"""LX1-b round 14: independent re-derivation of the L03 and L04 numbers (not using the twins' code).

Run: <checkout>/.venv/bin/python -I ledgers/LX1/scripts/LX1-b-r14/rederive_r14.py <checkout>
Exact arithmetic: fractions.Fraction for rates and model values; decimal (60 digits) for logarithms and roots.
"""
import csv
import sys
from decimal import Decimal, getcontext, ROUND_HALF_UP
from fractions import Fraction

getcontext().prec = 60
ROOT = sys.argv[1]


def q(x, places):
    return Decimal(x).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


def dec(fr):
    return Decimal(fr.numerator) / Decimal(fr.denominator)


# ---------- L04 ----------
rows = []
with open(f"{ROOT}/course/assets/data/market/fx_monthly.csv", encoding="utf-8", newline="") as h:
    rd = csv.reader(h)
    header = next(rd)
    gi = header.index("GBP")
    for r in rd:
        rows.append((r[0], r[gi]))
print("L04 rows", len(rows), "first", rows[0], "last", rows[-1])
blanks = [m for m, v in rows if v.strip() == ""]
print("L04 GBP blanks", len(blanks))
months = [m for m, _ in rows]
rates = {m: Fraction(v) for m, v in rows}
assert all(v > 0 for v in rates.values())
ch = []
for i in range(1, len(months)):
    a, b = months[i - 1], months[i]
    ratio = rates[b] / rates[a]
    ln = (dec(ratio)).ln()
    ch.append((b, ln, ratio == 1))
zeros = [m for m, _, z in ch if z]
print("L04 changes", len(ch), "zeros", len(zeros), zeros)
print("L04 nonzero", len(ch) - len(zeros))


def sd(vals):
    n = len(vals)
    mean = sum(vals, Decimal(0)) / n
    return (sum(((v - mean) ** 2 for v in vals), Decimal(0)) / (n - 1)).sqrt()


w1 = [ln for _, ln, _ in ch]
w2_items = [(m, ln) for m, ln, _ in ch if m >= "2000-01"]
w2 = [ln for _, ln in w2_items]
s1, s2 = sd(w1), sd(w2)
print("L04 n1", len(w1), "sd1", q(s1, 6), "exact", s1)
print("L04 n2", len(w2), "sd2", q(s2, 6), "exact", s2)
print("L04 diff unrounded", s2 - s1, "-> 6dp", q(s2 - s1, 6), "printed difference of rounded", q(s2, 6) - q(s1, 6))
print("L04 ratio", s2 / s1, "-> 4dp", q(s2 / s1, 4))
big1 = max(ch, key=lambda t: abs(t[1]))
big2 = max([c for c in ch if c[0] >= "2000-01"], key=lambda t: abs(t[1]))
print("L04 largest w1", big1[0], q(big1[1], 6), "abs", q(abs(big1[1]), 6))
print("L04 largest w2", big2[0], q(big2[1], 6), "abs", q(abs(big2[1]), 6))
# window two base month
print("L04 rate 1999-12", rates["1999-12"], "rate 2000-01", rates["2000-01"])
print("L04 1976-07 ratio", rates["1976-07"] / rates["1976-06"] if "1976-06" in rates else None)
print("L04 sum identity w1", q(sum(w1, Decimal(0)) - (dec(rates[months[-1]] / rates[months[0]])).ln(), 15))
print("L04 sum identity w2", q(sum(w2, Decimal(0)) - (dec(rates[months[-1]] / rates["1999-12"])).ln(), 15))
# quiz and page numbers
print("L04 ln1.1", q(Decimal("1.1").ln(), 10), "simple", Decimal("0.1"), "diff", q(Decimal("0.1") - Decimal("1.1").ln(), 6))
z = Decimal("0.135846")
print("L04 band h unrounded exact z", s1 and "", "tanh(z/2) =", q(((z.exp() - 1) / (z.exp() + 1)), 6))
for hh in (Decimal("0.0678"),):
    print("L04 bound h=0.0678 ln((1+h)/(1-h))", q(((1 + hh) / (1 - hh)).ln(), 6))
print("L04 E2 simple change for -0.0965747...", q((Decimal("-0.0965747")).exp() - 1, 6))
print("L04 M2 mean", q(Decimal("0.02") / 3, 6), "sd", q(((Fraction(19, 30000))).__float__() ** 0.5 * 1, 6))
print("L04 M2 exact var", Fraction(19, 30000), "sd", q(dec(Fraction(19, 30000)).sqrt(), 6))
print("L04 M3 months 2000-01..2026-09", (2026 - 2000) * 12 + (9 - 1) + 1)

# ---------- L03 ----------
D = 1_000_000
A0 = 4_000_000
H = 12
delta = Fraction(1, 50)


def path(m):
    out = []
    for t in range(H + 1):
        P = (1 - delta) ** min(t, m)
        V = Fraction(D) / P
        A = A0 - (V - D)
        L = V / A
        L0 = Fraction(D) / Fraction(A0)
        psi = L - L0
        out.append((t, P, V, A, L, psi))
    return out


def depth(m, phi=Fraction(1), beta=Fraction(1)):
    p = path(m)
    f = [beta * phi * x[5] for x in p]
    mx = max(f)
    first = next(t for t, v in zip(range(H + 1), f) if v == mx)
    return mx, first


for m in (12, 4):
    p = path(m)
    print(f"L03 economy m={m}")
    for t, P, V, A, L, psi in p:
        print(f"  t={t:2d} P={q(dec(P),4)} V_cents={q(dec(V),4)} V_round={int(q(dec(V),0))} A_round={int(q(dec(A),0))} L={q(dec(L),4)} psi={q(dec(psi),4)} fall%={q(dec(psi)*100,2)}")
dx, fx = depth(12)
dy, fy = depth(4)
print("L03 depth X exact pct", q(dec(dx) * 100, 6), "first", fx, "rounded", q(dec(dx) * 100, 2))
print("L03 depth Y exact pct", q(dec(dy) * 100, 6), "first", fy, "rounded", q(dec(dy) * 100, 2))
print("L03 difference exact pct", q(dec(dx - dy) * 100, 6), "-> 2dp", q(dec(dx - dy) * 100, 2), "printed diff of rounded", q(dec(dx) * 100, 2) - q(dec(dy) * 100, 2))
print("L03 ratio X/Y exact", q(dec(dx / dy), 6), "-> 4dp", q(dec(dx / dy), 4))
for phi in (Fraction(1, 2), Fraction(1), Fraction(3)):
    a, _ = depth(12, phi=phi)
    b, _ = depth(4, phi=phi)
    print("L03 ratio at phi", phi, "=", q(dec(a / b), 6))
print("L03 V_12 exact cents", q(dec(Fraction(D) / (Fraction(49, 50) ** 12)), 4))
print("L03 V_4 exact cents", q(dec(Fraction(D) / (Fraction(49, 50) ** 4)), 4), "P4 exact", Fraction(49, 50) ** 4)
p4 = path(4)[4]
print("L03 M2 A_4 exact", q(dec(p4[3]), 4), "M3 L_4 exact", q(dec(p4[4]), 6), "-> 4dp", q(dec(p4[4]), 4))
print("L03 leverage baseline", q(dec(Fraction(D) / Fraction(A0)), 4))
# depth monotone check and rise check
ds = [depth(m)[0] for m in range(H + 1)]
print("L03 depth never falls", all(ds[i] <= ds[i + 1] for i in range(H)), "rises every step", all(ds[i] < ds[i + 1] for i in range(H)))
print("L03 depths pct", [str(q(dec(d) * 100, 2)) for d in ds])
# lambda closed form check
C = A0 + D
lam = lambda x: x / (C - x)
for m in (4, 12):
    V = Fraction(D) / (Fraction(49, 50) ** m)
    closed = lam(V) - lam(Fraction(D))
    print("L03 closed form m", m, q(dec(closed) * 100, 6), "vs depth", q(dec(depth(m)[0]) * 100, 6))
print("L03 P4 check", Fraction(49, 50) ** 4 == Fraction(5764801, 6250000))
print("L03 E1 depth Y exact 2.6867 check", q(dec(dy) * 100, 4))
# Corollary 3.4 ratio closed form
r = (lam(Fraction(D) / (Fraction(49, 50) ** 12)) - lam(Fraction(D))) / (lam(Fraction(D) / (Fraction(49, 50) ** 4)) - lam(Fraction(D)))
print("L03 closed-form ratio", q(dec(r), 6))
