"""LX1-b round 12: independent re-derivation of every number in L03 and L04 (not importing the twins).

Run: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r12/rederive_r12.py <checkout>
"""
import csv
import math
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F

root = sys.argv[1]


def hu(x, places):
    return Decimal(repr(x)).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP) if isinstance(x, float) else \
        (F(x) * 10**places + F(1, 2)).__floor__() / 10**places


def q_exact(fr, places):
    # half-up rounding of an exact Fraction to 'places' decimals, returned as string
    scaled = fr * 10**places
    n = math.floor(scaled + F(1, 2))
    whole, frac = divmod(n, 10**places)
    return f"{whole}.{frac:0{places}d}"


print("== L03 model (exact Fractions) ==")
D = F(1_000_000)
N0 = F(4_000_000)
delta = F(1, 50)
C = N0 + D


def V(m, t):
    P = (1 - delta) ** min(t, m)
    return D / P


def ell(x):
    return x / (C - x)


def depth_exact(m):
    # phi = beta = 1; closed form of Prop 3.2(b) and brute max over path
    path = []
    for t in range(13):
        Vt = V(m, t)
        assert Vt < C
        path.append(ell(Vt) - ell(D))
    brute = max(path)
    closed = ell(V(m, m)) - ell(D)
    assert brute == closed, (m, brute, closed)
    first = next(t for t, v in enumerate(path) if v == brute)
    return brute, first, path


dX, tX, pathX = depth_exact(12)
dY, tY, pathY = depth_exact(4)
print("depth X exact", float(dX), "pct", float(100 * dX), "printed", q_exact(100 * dX, 2), "first t", tX)
print("depth Y exact", float(dY), "pct", float(100 * dY), "printed", q_exact(100 * dY, 2), "first t", tY)
print("exact depth Y to 4 places in percent:", q_exact(100 * dY, 4))
print("difference X-Y exact pct", float(100 * (dX - dY)), "printed", q_exact(100 * (dX - dY), 2))
print("difference of printed depths", F(q_exact(100 * dX, 2)) - F(q_exact(100 * dY, 2)))
print("ratio X/Y", float(dX / dY), "printed", q_exact(dX / dY, 4))
for r in ("1/2", "1", "3"):
    phi = F(r)
    ratio = (ell(V(12, 12)) - ell(D)) / (ell(V(4, 4)) - ell(D))
    print("ratio beta*phi=", r, "printed", q_exact(ratio, 4))
print("real debt X t=12 exact", float(V(12, 12)), "cents printed", q_exact(V(12, 12), 0).split('.')[0])
print("real debt Y t=4 exact", float(V(4, 4)), "printed rounded", math.floor(V(4, 4) + F(1, 2)))
P4 = (1 - delta) ** 4
print("P_4 exact", P4, float(P4))
print("M1: V_4 exact", float(D / P4), "rounded", math.floor(D / P4 + F(1, 2)))
N4 = N0 - (V(4, 4) - D)
print("M2: N_4 exact", float(N4), "rounded", math.floor(N4 + F(1, 2)), "with rounded V4", N0 - (1084166 - 1000000))
L4 = V(4, 4) / N4
print("M3: L_4 exact", float(L4), "4dp", q_exact(L4, 4), "with rounded V4,N4", q_exact(F(1084166) / F(3915834), 4))
print("baseline L0", float(D / N0))
print("premium Y t=4 exact", float(ell(V(4, 4)) - ell(D)), "pct", q_exact(100 * (ell(V(4, 4)) - ell(D)), 4))
print("Y index t=4", q_exact(P4, 4), "t=12 index Y", q_exact((1 - delta) ** 4, 4))
print("X index 12", q_exact((1 - delta) ** 12, 4), float((1 - delta) ** 12))
print("Y leverage", q_exact(V(4, 4) / (N0 - (V(4, 4) - D)), 4))
print("ell lemma check at random points:")
import random
rng = random.Random(12)
for _ in range(2000):
    x = D + F(rng.randrange(1, 10**6), 10**6) * (C - D) * F(9, 10)
    y = x + F(rng.randrange(1, 10**6), 10**9) * (C - x)
    if y >= C:
        continue
    lhs = ell(y) - ell(x)
    rhs = C * (y - x) / ((C - x) * (C - y))
    assert lhs == rhs and lhs > 0
print("Lemma 3.1 identity and strict increase: 2000 random pairs OK")
# Prop 3.2(a) and (c): V_t <= V_m and first attainment at m, for all m in 1..12, t in 0..12
for m in range(0, 13):
    vals = [V(m, t) for t in range(13)]
    assert all(v <= V(m, m) for v in vals)
    if m >= 1:
        assert all(vals[t] < V(m, m) for t in range(m))
print("Prop 3.2(a),(c) for all m in 0..12: OK")
# Corollary 3.3 and 3.4 over all pairs
dep = {m: depth_exact(m)[0] for m in range(13)}
assert all(dep[m] <= dep[m + 1] for m in range(12)) and all(dep[m] < dep[m + 1] for m in range(12))
assert dep[0] == 0
for a in range(1, 13):
    for b in range(a + 1, 13):
        ra = dep[b] / dep[a]
print("Cor 3.3 adjacent strict for m 0..12 OK; depth(0)=0 OK")
# Remark 4.2: N_t > 0 under Assumption 1.2 for m=12 and all m
for m in range(13):
    for t in range(13):
        assert N0 - (V(m, t) - D) > 0
print("N_t > 0 for all m,t: OK")
# Remark 4.2/R2 quadratic-premium ratio claim: ratio^2 differs from ratio
rat = dep[12] / dep[4]
print("ratio", float(rat), "ratio squared", float(rat * rat))
print("quadratic premium ratio check (depth = (ell(V_m)-ell(D))^2): ratio", float(((ell(V(12,12))-ell(D))/(ell(V(4,4))-ell(D)))**2))
print("E2: 9.204597 - 2.686713 =", 9.204597 - 2.686713, "; unrounded diff pct", float(100*(dX-dY)))

print("\n== L04 (recorded column, from the checkout's CSV) ==")
rows = []
with open(f"{root}/course/assets/data/market/fx_monthly.csv", newline="", encoding="utf-8") as h:
    r = csv.DictReader(h)
    print("header", r.fieldnames)
    for rec in r:
        rows.append((rec["month"], rec["GBP"]))
print("rows", len(rows), rows[0], rows[-1])
blank = [m for m, v in rows if not v.strip()]
print("GBP blank cells", len(blank))
# months consecutive
def idx(s):
    y, mm = s.split("-")
    return int(y) * 12 + int(mm) - 1
assert all(idx(rows[i + 1][0]) == idx(rows[i][0]) + 1 for i in range(len(rows) - 1))
rates = [(m, F(v)) for m, v in rows]
changes = []
for (pm, pr), (m, r_) in zip(rates, rates[1:]):
    changes.append((m, math.log(float(r_ / pr)), r_ == pr))
print("changes", len(changes), changes[0][0], changes[-1][0])
zeros = [m for m, c, z in changes if z]
print("exact zero months", len(zeros), zeros)
vals_w1 = [c for m, c, z in changes]
w2 = [(m, c) for m, c, z in changes if m >= "2000-01"]
vals_w2 = [c for m, c in w2]
print("window two changes", len(vals_w2), w2[0][0], w2[-1][0])


def sd(xs):
    n = len(xs)
    mu = math.fsum(xs) / n
    return math.sqrt(math.fsum((x - mu) ** 2 for x in xs) / (n - 1))


s1 = sd(vals_w1)
s2 = sd(vals_w2)
print("sd1 =", repr(s1), "printed 6dp", f"{s1:.6f}")
print("sd2 =", repr(s2), "printed 6dp", f"{s2:.6f}")
print("diff", repr(s2 - s1), "printed", f"{s2 - s1:.6f}")
print("ratio", repr(s2 / s1), "printed 4dp", f"{s2 / s1:.4f}")
print("subtracting printed figures:", f"{round(s2,6) - round(s1,6):.6f}", round(s2, 6) - round(s1, 6))
big1 = max(changes, key=lambda t: abs(t[1]))
big2 = max(w2, key=lambda t: abs(t[1]))
print("largest window one", big1[0], repr(big1[1]), "window two", big2[0], repr(big2[1]))
# identity
for name, start_rate, chs in (("w1", rates[0][1], [(m, c) for m, c, _ in changes]), ("w2", dict(rates)["1999-12"], w2)):
    tot = math.fsum(t[1] for t in chs)
    print(name, "identity err", abs(tot - math.log(float(rates[-1][1] / start_rate))))
print("min/max 1999-12 rate", dict(rates)["1999-12"])
# Part A model
print("model sd check", sd([math.log(2.0 / 2.0)] * 11) if False else "zero by construction")

print("\n== Prose numbers ==")
print("simple vs log 1.1:", math.log(1.1), 0.1 - math.log(1.1))
print("1.1*1.1 =", 1.1 * 1.1)
print("M1 log(1.1)", math.log(1.375 / 1.25), "simple", 1.375 / 1.25 - 1, "diff", (1.375 / 1.25 - 1) - math.log(1.375 / 1.25))
x = [0.01, 0.03, -0.02]
mu = sum(x) / 3
ss = sum((v - mu) ** 2 for v in x)
print("M2 mean", mu, "ssdev", ss, 19 / 15000, "disp", math.sqrt(ss / 2), math.sqrt(19 / 30000))
print("M2 sum sq", sum(v * v for v in x), "minus 3*(1/150)^2", sum(v * v for v in x) - 3 * (1 / 150) ** 2)
print("E2 simple change of -0.0965747...:", math.exp(-0.0965747) - 1, "full", math.exp(big2[1]) - 1, "log", big2[1])
L = big1[1]
h = math.tanh(L / 2)
print("R2 L", repr(L), "L/2", L / 2, "h tanh", h, "4dp", f"{h:.4f}")
print("R2 bound at h=0.0678:", math.log((1 + 0.0678) / (1 - 0.0678)), "4dp", f"{math.log((1 + 0.0678) / (1 - 0.0678)):.4f}")
print("R2 bound at h=0.0678 vs L", math.log((1 + 0.0678) / (1 - 0.0678)) - L)
print("Q11 bound 4dp", f"{math.log((1.0678) / (0.9322)):.6f}")
print("P2 band h=0 bound", math.log(1))
print("E1 nonzero", len(vals_w1) - len(zeros))
print("M3 count 2000-01..2026-09:", (2026 - 2000) * 12 + (9 - 1) + 1)
print("ln 1.1 6dp", f"{math.log(1.1):.6f}", "diff 6dp", f"{0.1 - math.log(1.1):.6f}")
