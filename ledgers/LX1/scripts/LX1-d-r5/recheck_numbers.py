"""Independent re-derivation of every number on the LX1 cards (slice d, round 5). Standard library only."""
import csv, math, random, sys
from fractions import Fraction as Fr
from decimal import Decimal, ROUND_HALF_UP

def rhu(x):  # half-up to whole number for Fraction
    return math.floor(x + Fr(1, 2))

out = []
def say(k, v):
    out.append(f"{k}: {v}")

# ---- L01 (cards c002-c005, c009-c013, c025 area not here)
d1 = Fr(400); r = Fr(9, 100); g = Fr(3, 100); gp = Fr(1, 100)
F0 = d1 / (r - g)
say("L01 F0 exact", F0)
say("L01 F0 rounded", rhu(F0))
q = (1 + g) / (1 + r)
say("L01 q", q)
say("L01 0<q<1", 0 < q < 1)
for N in (10, 60, 200, 400):
    SN = sum(d1 * (1 + g) ** (s - 1) / (1 + r) ** s for s in range(1, N + 1))
    say(f"L01 identity N={N}", SN == F0 * (1 - q ** N))
# c012: single dividend 400 at t=0 with no later dividends
say("L01 c012 PV single dividend", Fr(400) / (1 + r))
say("L01 c012 PV rounded", rhu(Fr(400) / (1 + r)))
say("L01 c012 formula at g=3% rounded", rhu(F0))
# c011: witness
F0_1 = d1 / (r - Fr(1, 100)); F0_3 = d1 / (r - Fr(3, 100))
say("L01 witness F0(1%)", F0_1); say("L01 witness F0(3%)", F0_3)
say("L01 witness gap at 6000 under 1%", 6000 - F0_1); say("L01 witness gap at 6000 under 3%", Fr(6000) - F0_3)
# c005 / c013: partial sums diverge for g>=r  (g=r=5%, d1=100)
S10 = sum(Fr(100) * Fr(1, 1) ** (s - 1) / Fr(105, 100) ** s for s in range(1, 11))
say("L01 mech3 S10 at g=r=5%", S10)

# ---- L02 (c015-c025, c066, c073-c074)
D = 1_000_000
# c024/c025/c066: re-derive the seeded path with the same generator, independently
rng = random.Random(20261104)
P = [Fr(100)]
ch = []
for _ in range(12):
    c = rng.randint(-4, 3); ch.append(c); P.append(P[-1] * (1 + Fr(c, 100)))
V = [Fr(D) * 100 / p for p in P]
rounded = [rhu(v) for v in V]
say("L02 changes", ch)
say("L02 real values rounded", rounded)
say("L02 consecutive real values all differ", all(rounded[t] != rounded[t - 1] for t in range(1, 13)))
say("L02 identity all t", all(V[t] / V[t - 1] == P[t - 1] / P[t] for t in range(1, 13)))
falls = [t for t in range(1, 13) if P[t] < P[t - 1]]
rises = [t for t in range(1, 13) if V[t] > V[t - 1]]
say("L02 falls", falls); say("L02 rises", rises); say("L02 falls==rises", falls == rises)
# c015/c016 Prop 1.2 value check
kap = Fr(2, 5); say("L02 gram price", 1 / kap)
# M1/M2/M3 and E2/E3 numbers
say("L02 E2 V1 with P1=99 rounded", rhu(Fr(1000000) * 100 / 99))
say("L02 E3 P0/P12 exact", float(P[0] / P[12]))
say("L02 P12 exact", float(P[12]))
say("L02 M3 V1 (2000/95)", float(Fr(2000) * 100 / 95))
# c022 factor sanity M1: 100/80
say("L02 M1 V1", Fr(2000) * 100 / 80)

# ---- L03 (c026-c047, c067, c071-c072)
DEBT = Fr(1_000_000); N0 = Fr(4_000_000); C = N0 + DEBT
delta = Fr(1, 50)
def ell(x): return x / (C - x)
def path(m): return [DEBT / (1 - delta) ** min(t, m) for t in range(13)]
def depth(m, phi=Fr(1), beta=Fr(1)):
    Vs = path(m)
    fs = [beta * phi * (ell(v) - ell(DEBT)) for v in Vs]
    return max(fs), fs.index(max(fs))
dX, tX = depth(12); dY, tY = depth(4)
say("L03 depth X exact (fraction)", float(dX)); say("L03 depth X percent 2dp", Decimal(str(float(dX) * 100)).quantize(Decimal('0.01'), ROUND_HALF_UP))
say("L03 depth X first t", tX)
say("L03 depth Y exact (fraction)", float(dY)); say("L03 depth Y percent 2dp", Decimal(str(float(dY) * 100)).quantize(Decimal('0.01'), ROUND_HALF_UP))
say("L03 depth Y first t", tY)
say("L03 X minus Y exact percent", float((dX - dY) * 100))
for phi, beta in ((Fr(1, 2), Fr(1)), (Fr(1), Fr(1)), (Fr(3), Fr(1)), (Fr(1), Fr(2))):
    rr = depth(12, phi, beta)[0] / depth(4, phi, beta)[0]
    say(f"L03 ratio X/Y phi={phi} beta={beta} exact", float(rr))
say("L03 ratio exact fraction(Cor 3.4 formula)", float((ell(path(12)[12]) - ell(DEBT)) / (ell(path(4)[4]) - ell(DEBT))))
say("L03 V12 exact cents", float(path(12)[12]))
say("L03 V4 exact cents", float(path(4)[4]))
say("L03 P4 exact", str((Fr(49, 50)) ** 4))
say("L03 N4 Y exact", float(N0 - (path(4)[4] - DEBT)))
say("L03 L4 Y exact", float(path(4)[4] / (N0 - (path(4)[4] - DEBT))))
say("L03 depth(0)", depth(0)[0])
mono = [depth(m)[0] for m in range(13)]
say("L03 depth strictly rising each step", all(mono[m] < mono[m + 1] for m in range(12)))
say("L03 leverage baseline", float(DEBT / N0))
say("L03 cards c035 depth(4)<depth(12)", depth(4)[0] < depth(12)[0])
# c040 eq. Lab 1 Part A X at t=12 real debt rounded
say("L03 c047 V12 rounded", rhu(path(12)[12]))

# ---- L04 (c048-c070)
rows = []
with open("/Users/billyribeiro/.fanout/wt/verifyE5-LX1-d/course/assets/data/market/fx_monthly.csv", newline="", encoding="utf-8") as h:
    rd = csv.DictReader(h)
    fields = rd.fieldnames
    for rec in rd:
        rows.append((rec["month"], rec["GBP"]))
say("L04 header", fields)
blank = [m for m, v in rows if v.strip() == ""]
say("L04 blank GBP cells", blank)
months = [m for m, _ in rows]
say("L04 n months", len(rows)); say("L04 first/last", (months[0], months[-1]))
# consecutive
def mi(m): y, mm = int(m[:4]), int(m[5:]); return 12 * y + mm - 1
say("L04 consecutive months", all(mi(months[i]) == mi(months[i - 1]) + 1 for i in range(1, len(months))))
rate = {m: Fr(v) for m, v in rows}
chg = []
for i in range(1, len(rows)):
    m0, v0 = rows[i - 1]; m1, v1 = rows[i]
    chg.append((m1, math.log(float(Fr(v1) / Fr(v0)))))
zeros = [m for i, (m, c) in enumerate(chg) if rows[i + 1][1] == rows[i][1]]
say("L04 zero-change months", zeros)
say("L04 zero count window one", len(zeros))
say("L04 nonzero window one", sum(1 for _, c in chg if c != 0.0))
def sd(vals):
    n = len(vals); mu = math.fsum(vals) / n
    return math.sqrt(math.fsum((v - mu) ** 2 for v in vals) / (n - 1))
w1 = [c for _, c in chg]
w2 = [c for m, c in chg if m >= "2000-01"]
say("L04 n window one", len(w1)); say("L04 n window two", len(w2))
s1, s2 = sd(w1), sd(w2)
say("L04 sd window one", f"{s1:.12f}")
say("L04 sd window two", f"{s2:.12f}")
say("L04 sd diff (unrounded)", f"{s2 - s1:.12f}")
say("L04 sd ratio", f"{s2 / s1:.10f}")
say("L04 diff of rounded printed", round(s2, 6) - round(s1, 6))
mx1 = max(chg, key=lambda t: abs(t[1])); mx2 = max([t for t in chg if t[0] >= "2000-01"], key=lambda t: abs(t[1]))
say("L04 max window one", mx1); say("L04 max window two", mx2)
say("L04 ln(1.1)", f"{math.log(1.1):.12f}")
say("L04 ln(1.1)-0.1", f"{0.1 - math.log(1.1):.12f}")
say("L04 R2 h=0.0678 bound", f"{math.log((1 + 0.0678) / (1 - 0.0678)):.12f}")
say("L04 R2 exact h for L=|max1|", f"{math.tanh(abs(mx1[1]) / 2):.12f}")
say("L04 simple change at 2008-10 from log", f"{math.exp(mx2[1]) - 1:.12f}")
say("L04 M1 simple vs log", f"{1.375/1.25 - 1:.12f} {math.log(1.375/1.25):.12f}")
say("L04 M2 sd of three changes", f"{sd([0.01, 0.03, -0.02]):.12f}")
say("L04 M3 months 2000-01..2026-09", (2026 - 2000) * 12 + 9)
say("L04 window one 2026-09 last value", rows[-1])

print("\n".join(out))
