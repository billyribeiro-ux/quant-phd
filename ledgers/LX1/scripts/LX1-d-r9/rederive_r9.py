"""Round-9 independent re-derivation of the numbers the LX1 cards state (slice d, verifier).

Run: python -I <this file>. Uses only the standard library and the embedded snapshot
course/assets/data/market/fx_monthly.csv (read from the repository path given below).
Written from the lesson formulas, not from the lab source.
"""
import csv
import math
import random
from fractions import Fraction as Fr
from decimal import Decimal, ROUND_HALF_UP

def rhu(x):  # round half up to a whole number, exact input
    return math.floor(Fr(x) + Fr(1, 2))

def rhu_dec(x, places):
    return Decimal(repr(x)).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)

out = []
def say(label, value):
    out.append(f"{label}: {value}")

# ---- L01 closed form (c002, c003, c004, c007, c011, c012, c013)
d1, r, g = Fr(400), Fr(9, 100), Fr(3, 100)
F0 = d1 / (r - g)
say("c002 F_0 = d1/(r-g) (exact)", F0)
say("c002 F_0 rounded half up", rhu(F0))
q = (1 + g) / (1 + r)
say("c004 q = (1+g)/(1+r)", q)
say("c004 0<q<1", 0 < q < 1)
ok = True
for N in range(1, 201):
    S = sum(d1 * (1 + g) ** (s - 1) / (1 + r) ** s for s in range(1, N + 1))
    ok = ok and (S == F0 * (1 - q ** N))
say("c003 identity S_N = F_0(1-q^N) exact for N=1..200", ok)
for t in (0, 1, 5):
    Ft = d1 * (1 + g) ** t / (r - g)
    St = sum(d1 * (1 + g) ** (t + k - 1) / (1 + r) ** k for k in range(1, 201))
    say(f"c002/c004 F_{t} vs 200-term partial sum rounded diff (cents)", float(St - Ft))
g1 = Fr(1, 100)
F0_g1 = d1 / (r - g1)
say("c011 F_0(1%) exact", F0_g1)
say("c011 gap at P0=6000 under 1% (cents)", 6000 - F0_g1)
say("c011 gap at P0=6000 under 3% (cents)", 6000 - F0)
say("c007 F_0(g=1%) < F_0(g=3%)", F0_g1 < F0)
say("c012 PV 400/1.09 exact", Fr(400) / (1 + r))
say("c012 PV rounded", rhu(Fr(400) / (1 + r)))
say("c013 (A2) g=10%>=r: each term k=1..50 >= d1/(1+r) (g=1% is outside A2, not tested)", all(d1 * (1 + Fr(10,100)) ** (k - 1) / (1 + r) ** k >= d1 / (1 + r) for k in range(1, 51)))
gg = Fr(9, 100)  # g = r boundary of (A2)
say("c013 (A2) g=r=9%: each term k=1..50 >= d1/(1+r)", all(d1 * (1 + gg) ** (k - 1) / (1 + r) ** k >= d1 / (1 + r) for k in range(1, 51)))

# ---- L01 lab Part B/C (c009, c010) with the lab's seeded draws (the lab's own draw rule)
SEED = 20261103
def fundamental(growth, t):
    return d1 * (1 + growth) ** t / (r - growth)
rng = random.Random(SEED)
gaps3, prices = [], []
for t in range(13):
    w = Fr(rng.randint(-8, 25), 100)
    price = rhu(fundamental(g, t) * (1 + w))
    prices.append(price)
    gaps3.append(price - rhu(fundamental(g, t)))
say("c009 periods price > fundamental at 3% (of 13)", sum(1 for x in gaps3 if x > 0))
rng = random.Random(SEED)
cnt1 = 0
for t in range(13):
    w = Fr(rng.randint(-8, 25), 100)
    price = rhu(fundamental(g, t) * (1 + w))
    cnt1 += price - rhu(fundamental(g1, t)) > 0
say("c010 periods price > alternative fundamental at 1% (of 13)", cnt1)

# ---- L02 (c024, c025, c066): real value path
DEBT = 1_000_000
base = Fr(100)
rng = random.Random(20261104)
P = [base]
for _ in range(12):
    c = rng.randint(-4, 3)
    P.append(P[-1] * (1 + Fr(c, 100)))
V = [Fr(DEBT) * base / p for p in P]
Vc = [rhu(v) for v in V]
say("c024 V_t changes in each of 12 periods (cents differences nonzero)", all(Vc[t] != Vc[t - 1] for t in range(1, 13)))
say("c025 identity V_t/V_(t-1)=P_(t-1)/P_t exact for t=1..12", all(V[t] / V[t - 1] == P[t - 1] / P[t] for t in range(1, 13)))
falls = [t for t in range(1, 13) if P[t] < P[t - 1]]
rises = [t for t in range(1, 13) if V[t] > V[t - 1]]
say("c066 falls count / rises count", (len(falls), len(rises)))
say("c066 falling-index set equals rising-real-value set", falls == rises)
say("c066 V_1 cents (c011 of L02 cross-check: 1010101)", Vc[1])
say("c066 V_12 / V_0 to 6 dp (E3)", rhu_dec(float(V[12] / V[0]), 6))

# ---- L03 closed form (c032, c033, c035, c036, c037, c038, c039, c046)
D = Fr(1_000_000); N0 = Fr(4_000_000); delta = Fr(1, 50); H = 12
def ell(x):
    C = N0 + D
    return x / (C - x)
def depth_closed(m, phi=Fr(1), beta=Fr(1)):
    Vm = D * (1 - delta) ** (-m)
    return beta * phi * (ell(Vm) - ell(D))
def depth_direct(m, phi=Fr(1), beta=Fr(1)):
    vals = []
    for t in range(H + 1):
        Pt = (1 - delta) ** min(t, m)
        Vt = D / Pt
        Nt = N0 - (Vt - D)
        Lt = Vt / Nt
        L0 = D / N0
        vals.append(beta * phi * (Lt - L0))
    return max(vals), vals.index(max(vals))
for m in range(0, 13):
    if m == 0:
        assert depth_closed(0) == 0
    dd, first = depth_direct(m)
    assert dd == depth_closed(m), m
say("c032 closed form equals direct max for m=0..12 (exact)", True)
say("c034 depth(0) exact", depth_direct(0))
dX, fX = depth_direct(12); dY, fY = depth_direct(4)
say("c037 depth X exact (percent)", float(100 * dX))
say("c037 X first attained t", fX)
say("c038 depth Y exact (percent)", float(100 * dY))
say("c038 Y first attained t", fY)
say("c039 ratio X/Y exact", float(dX / dY))
say("c039 ratio X/Y rounded 4dp", rhu_dec(float(dX / dY), 4))
say("c039 ratio closed form equals (ell(V12)-ell(D))/(ell(V4)-ell(D))", dX / dY == (ell(D * (1 - delta) ** -12) - ell(D)) / (ell(D * (1 - delta) ** -4) - ell(D)))
for phi, beta in ((Fr(1, 2), Fr(1)), (Fr(1), Fr(1)), (Fr(3), Fr(1))):
    say(f"c067 ratio X/Y at phi={phi} beta={beta}", float(depth_direct(12, phi, beta)[0] / depth_direct(4, phi, beta)[0]))
say("c046 depth scales with beta (beta=2 vs 1 ratio)", depth_direct(12, Fr(1), Fr(2))[0] / depth_direct(12, Fr(1), Fr(1))[0])
say("c035 depth(4) < depth(12)", depth_direct(4)[0] < depth_direct(12)[0])
say("c033 first attained at t=m for m=12 (first index)", depth_direct(12)[1])
say("c036 depth(12)/depth(4) equals closed ratio", depth_direct(12)[0] / depth_direct(4)[0] == (ell(D*(1-delta)**-12)-ell(D))/(ell(D*(1-delta)**-4)-ell(D)))
say("L03 difference X-Y exact percentage points", float(100 * (dX - dY)))
say("L03 difference of rounded printed depths", Fr("9.20") - Fr("2.69"))

# ---- L04 data (c054-c058, c063-c065, c068, c069, c075)
rows = []
with open("course/assets/data/market/fx_monthly.csv", encoding="utf-8", newline="") as h:
    rd = csv.DictReader(h)
    fields = rd.fieldnames
    for rec in rd:
        rows.append((rec["month"], rec["GBP"]))
say("c070 fx_monthly header columns", fields)
say("c069 months read / first / last", (len(rows), rows[0][0], rows[-1][0]))
rates = [(m, Fr(v)) for m, v in rows]
chg = [(rates[i][0], math.log(float(rates[i][1] / rates[i - 1][1]))) for i in range(1, len(rates))]
zeros = [rates[i][0] for i in range(1, len(rates)) if rates[i][1] == rates[i - 1][1]]
say("c054 exactly-zero changes (count, months)", (len(zeros), zeros))
say("c068 nonzero changes in window one", len(chg) - len(zeros))
def sd(xs):
    n = len(xs); m = math.fsum(xs) / n
    return math.sqrt(math.fsum((x - m) ** 2 for x in xs) / (n - 1))
w1 = [c for _, c in chg]
w2c = [(m, c) for m, c in chg if m >= "2000-01"]
say("c055 window one n, sd (6dp)", (len(w1), round(sd(w1), 9)))
say("c056 window two n, sd", (len(w2c), round(sd([c for _, c in w2c]), 9)))
say("c057 sd2/sd1 4dp", round(sd([c for _, c in w2c]) / sd(w1), 4))
say("c065 sd2 - sd1 (unrounded, 6dp)", round(sd([c for _, c in w2c]) - sd(w1), 9))
big1 = max(chg, key=lambda x: abs(x[1]))
big2 = max(w2c, key=lambda x: abs(x[1]))
say("c058 window two largest |change| month and signed", (big2[0], big2[1]))
say("L04 window one largest |change| month and signed", (big1[0], big1[1]))
say("c063 window two first change uses 1999-12 rate", rates[[m for m, _ in rates].index("2000-01") - 1][0])
say("c069/c075 fx_monthly rows contain only the month/GBP columns in header", fields)

# ---- model check
say("c029/c047 n/a (text claims)", "n/a")

print("\n".join(out))
