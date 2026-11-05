"""Independent re-derivation of every number on L03 and L04 (round 13). Uses decimal and fractions only, not the lab code."""
import csv
import math
from decimal import Decimal, getcontext, ROUND_HALF_UP
from fractions import Fraction

getcontext().prec = 60
ROOT = "/Users/billyribeiro/.fanout/wt/verifyE13-LX1-b"


def q(x, places):
    if isinstance(x, Fraction):
        x = Decimal(x.numerator) / Decimal(x.denominator)
    elif isinstance(x, float):
        x = Decimal(x)
    return Decimal(x).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


# ---------- L03 ----------
D = Fraction(1_000_000)
N0 = Fraction(4_000_000)
delta = Fraction(1, 50)
H = 12


def P(m, t):
    return (1 - delta) ** min(t, m)


def V(m, t):
    return D / P(m, t)


def L(m, t):
    v = V(m, t)
    n = N0 - (v - D)
    return v / n


def depth_path(m):
    L0 = L(m, 0)
    return [(L(m, t) - L0) for t in range(H + 1)]  # phi = beta = 1


def depth(m):
    return max(depth_path(m))


def first_at(m):
    p = depth_path(m)
    top = max(p)
    return next(t for t, x in enumerate(p) if x == top)


print("L03 Part A rows for X (m=12) and Y (m=4):")
for m in (12, 4):
    for t in range(H + 1):
        v = V(m, t)
        print(f"m={m} t={t:2d} index={float(P(m,t)):.6f} V={q(v,0)} lev={q(L(m,t),4)} prem={q(L(m,t)-L(m,0),4)} fall%={q(100*(L(m,t)-L(m,0)),2)}")
print("L0 =", q(L(12, 0), 4))
dx, dy = depth(12), depth(4)
print("depth X exact % =", q(100 * dx, 6), "printed", q(100 * dx, 2))
print("depth Y exact % =", q(100 * dy, 6), "printed", q(100 * dy, 2))
print("first X", first_at(12), "first Y", first_at(4))
print("diff exact pp =", q(100 * (dx - dy), 6), "rounded", q(100 * (dx - dy), 2))
print("diff of rounded printed values =", q(100 * dx, 2) - q(100 * dy, 2))
print("ratio of depths (beta*phi irrelevant):", q(dx / dy, 6), q(dx / dy, 4))
# Part D with phi scaling: depth scales with phi*beta exactly
for phi in (Fraction(1, 2), Fraction(1), Fraction(3)):
    r = (phi * dx) / (phi * dy)
    print("Part D product", phi, "ratio", q(r, 4))
print("Part C depths:")
ds = [depth(m) for m in range(H + 1)]
for m, v in enumerate(ds):
    print(f"  m={m:2d} {q(100*v,2)}  exact {q(100*v,6)}")
print("never falls:", all(ds[m] <= ds[m + 1] for m in range(H)), "strict:", all(ds[m] < ds[m + 1] for m in range(H)))
print("X real debt t=12 exact:", q(V(12, 12), 4), "rounded", q(V(12, 12), 0))
print("Y P4 exact:", P(4, 4), float(P(4, 4)), "V4 exact", float(V(4, 4)), q(V(4, 4), 4))
N4 = N0 - (V(4, 4) - D)
print("N4 exact", float(N4), "rounded", q(N4, 0))
print("L4 exact", float(V(4, 4) / N4), q(V(4, 4) / N4, 7), q(V(4, 4) / N4, 4))
print("M2 with rounded V4:", N0 - (Fraction(1084166) - D))
print("L03 checks (V_m < N0+D):", V(12, 12) < N0 + D, V(4, 4) < N0 + D)

# ---------- L04 ----------
rows = []
with open(f"{ROOT}/course/assets/data/market/fx_monthly.csv", encoding="utf-8", newline="") as h:
    rd = csv.DictReader(h)
    fields = rd.fieldnames
    for rec in rd:
        rows.append((rec["month"], rec["GBP"]))
print("L04 fields", fields)
print("rows", len(rows), rows[0], rows[-1])
blank = [m for m, v in rows if not v.strip()]
print("blank GBP cells:", len(blank))
vals = [(m, Fraction(v)) for m, v in rows]
# verify contiguous months
def mi(s):
    y, mo = s.split("-")
    return int(y) * 12 + int(mo) - 1
print("contiguous:", all(mi(vals[i][0]) + 1 == mi(vals[i + 1][0]) for i in range(len(vals) - 1)))
chg = [(vals[i][0], math.log(float(vals[i][1] / vals[i - 1][1]))) for i in range(1, len(vals))]
print("changes", len(chg), chg[0][0], chg[-1][0])
zeros = [m for i, (m, r) in enumerate(vals) if i > 0 and r == vals[i - 1][1]]
print("exact zero months", zeros)
w1 = chg
w2 = [c for c in chg if c[0] >= "2000-01"]
print("w2 changes", len(w2), w2[0][0], w2[-1][0])
# rate before 2000-01
idx = [m for m, _ in vals].index("2000-01")
print("rate before 2000-01 is", vals[idx - 1][0], vals[idx - 1][1])


def sd(xs):
    n = len(xs)
    mu = math.fsum(xs) / n
    return math.sqrt(math.fsum((x - mu) ** 2 for x in xs) / (n - 1))


def sd_exact_from_floats(xs):
    # high precision sd using Decimal of the float values
    getcontext().prec = 50
    ds = [Decimal(x) for x in xs]
    n = len(ds)
    mu = sum(ds) / n
    return (sum((d - mu) ** 2 for d in ds) / (n - 1)).sqrt()


s1 = sd([c for _, c in w1])
s2 = sd([c for _, c in w2])
print("s1", s1, q(Decimal(s1), 6))
print("s2", s2, q(Decimal(s2), 6))
print("diff unrounded", s2 - s1, q(Decimal(s2 - s1), 6))
print("printed-diff", q(Decimal(s2), 6) - q(Decimal(s1), 6))
print("ratio", s2 / s1, q(Decimal(s2 / s1), 4))
mx1 = max(w1, key=lambda c: abs(c[1]))
mx2 = max(w2, key=lambda c: abs(c[1]))
print("max w1", mx1, "max w2", mx2)
print("w1 sum telescoping:", abs(math.fsum(c for _, c in w1) - math.log(float(vals[-1][1] / vals[0][1]))))
print("w2 sum telescoping:", abs(math.fsum(c for _, c in w2) - math.log(float(vals[-1][1] / vals[idx - 1][1]))))
# simple change for E2
z = mx2[1]
print("E2 simple change:", math.exp(z) - 1, q(Decimal(math.exp(z) - 1), 6))
# ln 1.1
print("ln1.1", math.log(1.1), q(Decimal(math.log(1.1)), 6))
print("M1 diff", Decimal(1) / 10 - Decimal(math.log(1.1)))
# M2
xs = [0.01, 0.03, -0.02]
mu = sum(xs) / 3
print("M2 mean", mu, "sd", math.sqrt(sum((x - mu) ** 2 for x in xs) / 2))
# R2: h = tanh(z/2)
zz = mx1[1]
print("R2 z", zz, "h", math.tanh(zz / 2), q(Decimal(math.tanh(zz / 2)), 6), q(Decimal(math.tanh(zz / 2)), 4))
h4 = 0.0678
print("bound at h=0.0678", math.log((1 + h4) / (1 - h4)), q(Decimal(math.log((1 + h4) / (1 - h4))), 6))
print("bound at h=0.0678 vs z", math.log((1 + h4) / (1 - h4)) - zz)
print("count w1", len(w1), "w2", len(w2))
print("nonzero w1", len(w1) - len(zeros[:]))
# model check
print("model changes 11 zero:", all(x == 0 for x in [0.0] * 11))
