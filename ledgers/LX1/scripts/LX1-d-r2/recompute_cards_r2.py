"""Independent recomputation of every number on the LX1 cards and their lesson prose (round 2, slice d).

Run: python -I <this file> <repo root>. Uses fractions, math and csv only. Writes to stdout.
Each block names the card ids it supports.
"""
import csv
import math
import random
import sys
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(sys.argv[1])


def half_up(x: F) -> int:
    return math.floor(x + F(1, 2))


def r2(x: float, places: int) -> str:
    return str(Decimal(x).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))


print("== L01 (c002-c005, c009-c012, L01 quiz/Research numbers)")
d1, r, g = F(400), F(9, 100), F(3, 100)
F0 = d1 / (r - g)
print("F0 exact", F0, float(F0), "rounded", half_up(F0))
print("40000/109 =", F(40000, 109), float(F(40000, 109)), "rounded", half_up(F(40000, 109)), "(c012 says 367)")
print("F2 =", float(d1 * (1 + g) ** 2 / (r - g)), "rounded", half_up(d1 * (1 + g) ** 2 / (r - g)), "(quiz says 7073)")
q = (1 + g) / (1 + r)
print("q =", q, float(q), "(quiz 103/109 = 0.944954)")
for N in (10, 60, 200):
    S = sum(d1 * (1 + g) ** (s - 1) / (1 + r) ** s for s in range(1, N + 1))
    print("N", N, "S_N", float(S), "identity exact", S == F0 * (1 - q**N), "residual F0 q^N", float(F0 * q**N))
print("L01 Mechanics1: 250/0.06 =", F(250) / F(6, 100), "Mech2 F3 =", float(F(250) * F(104, 100) ** 3 / F(6, 100)))
print("Mech3 S10 with q=1 (r=g=5%):", float(sum(F(100) / F(105, 100) for _ in range(10))), "=", float(F(20000, 21)))
print("Empirical3: 2175/8698 =", float(F(2175, 8698)) * 100, "% ; unrounded fund t=9:", float(F(400) * F(103, 100) ** 9 / F(6, 100)))
print("Research1 g* =", float(F(9, 100) - F(400, 6000)), "2.33% ok")
print("witness: F0(1%) =", float(F(400) / F(8, 100)), " F0(3%) =", float(F(20000, 3)), " gap at 6000 under 1%:", 6000 - 5000, " under 3%:", float(6000 - F(20000, 3)))

# seeded Lab 1 L01 path, reimplemented independently (same seed and draws as the twin)
SEED = 20261103
rng = random.Random(SEED)
fund = [F(400) * F(103, 100) ** t / F(6, 100) for t in range(13)]
gaps3, wedges = [], []
for t in range(13):
    w = F(rng.randint(-8, 25), 100)
    wedges.append(w)
    price = half_up(fund[t] * (1 + w))
    gaps3.append(price - half_up(fund[t]))
print("L01 gaps (3%):", gaps3, "positive count", sum(1 for x in gaps3 if x > 0), "of 13 (c009: 9 of 13)")
rngB = random.Random(SEED)
altfund = [F(400) * F(101, 100) ** t / F(8, 100) for t in range(13)]
# alternative fundamental uses the 1% growth closed form: d1 (1+g')^t / (r - g')
altfund = [F(400) * F(101, 100) ** t / (F(9, 100) - F(1, 100)) for t in range(13)]
alt_pos = 0
for t in range(13):
    w = F(rngB.randint(-8, 25), 100)
    price = half_up(fund[t] * (1 + w))
    alt_pos += (price - half_up(altfund[t])) > 0
print("L01 alt count:", alt_pos, "of 13 (c010: 13 of 13)")

print("== L02 (c018-c025)")
SEED2 = 20261104
rng2 = random.Random(SEED2)
P = [F(100)]
ch = []
for _ in range(12):
    c = rng2.randint(-4, 3)
    ch.append(c)
    P.append(P[-1] * (1 + F(c, 100)))
V = [F(1_000_000) * F(100) / p for p in P]
falls = [t for t in range(1, 13) if P[t] < P[t - 1]]
rises = [t for t in range(1, 13) if V[t] > V[t - 1]]
print("changes", ch)
print("falls", falls, len(falls), "rises", rises, len(rises), "equal", falls == rises)
print("V rounded", [half_up(v) for v in V])
print("all consecutive real values differ:", all(V[t] != V[t - 1] for t in range(1, 13)))
print("identity exact all t:", all(V[t] / V[t - 1] == P[t - 1] / P[t] for t in range(1, 13)))
print("P12 unrounded", float(P[12]), "P0/P12 =", float(P[0] / P[12]), "six dp", r2(float(P[0] / P[12]), 6))
print("M1 V1 = 2000*100/80 =", F(2000 * 100, 80), "; M3 V1 = 200000/95 =", float(F(200000, 95)), "round", half_up(F(200000, 95)))
print("E2 V1 = 1000000*100/99 =", float(F(10**8, 99)), "round", half_up(F(10**8, 99)))
print("M2 V2/V1 = 90/85 =", F(90, 85))

print("== L03 (c029-c039, c046)")
D, N0, delta, H = 1_000_000, 4_000_000, F(1, 50), 12
C = N0 + D


def ell(x: F) -> F:
    return x / (C - x)


def depth(m: int, phi: F = F(1), beta: F = F(1)) -> F:
    vals = []
    for t in range(H + 1):
        Pt = (1 - delta) ** min(t, m)
        Vt = F(D) / Pt
        Lt = Vt / (C - Vt)
        L0 = F(D) / N0
        vals.append(beta * phi * (Lt - L0))
    return max(vals)


def first_t(m: int) -> int:
    vals = []
    for t in range(H + 1):
        Pt = (1 - delta) ** min(t, m)
        Vt = F(D) / Pt
        vals.append(F(Vt) / (C - Vt) - F(D) / N0)
    top = max(vals)
    return next(t for t, v in enumerate(vals) if v == top)


dX, dY = depth(12), depth(4)
print("depth(12) =", float(dX) * 100, "% ; depth(4) =", float(dY) * 100, "%")
print("first t X", first_t(12), "first t Y", first_t(4))
print("closed form depth(12) via ell:", float(ell(F(D) / (1 - delta) ** 12) - ell(F(D))) * 100)
print("ratio X/Y exact =", float(dX / dY), "4dp", r2(float(dX / dY), 4), "(c039 says 3.4260)")
for phi, beta in ((F(1, 2), F(1)), (F(1), F(1)), (F(3), F(1))):
    print("ratio phi,beta", phi, beta, float(depth(12, phi, beta) / depth(4, phi, beta)))
print("difference X-Y unrounded %:", float(dX - dY) * 100, "; rounded difference of printed:", round(9.20 - 2.69, 2))
print("depth(m) monotone nondecreasing, strict each step:", all(depth(m) < depth(m + 1) for m in range(12)))
print("M1 P4 =", (F(49, 50)) ** 4, float((F(49, 50)) ** 4), " V4 =", float(F(D) / (F(49, 50) ** 4)), "N4 =", float(N0 - (F(D) / (F(49, 50) ** 4) - D)))
print("L03 X real debt at 12 exact:", float(F(D) / (1 - delta) ** 12))
print("E3: unchanged index for economy Y, periods t=1..12 with P equal to previous:", sum(1 for t in range(1, 13) if (1 - delta) ** min(t, 4) == (1 - delta) ** min(t - 1, 4)))

print("== L04 (c048-c065) from the embedded CSV")
path = ROOT / "course/assets/data/market/fx_monthly.csv"
with path.open(encoding="utf-8", newline="") as h:
    rows = list(csv.DictReader(h))
print("rows", len(rows), rows[0]["month"], rows[-1]["month"])
gbp = []
for row in rows:
    cell = row["GBP"]
    if not cell or not all(ch in "0123456789." for ch in cell):
        raise SystemExit(f"blank or non-decimal GBP cell at {row['month']}")
    gbp.append((row["month"], F(cell)))
logs = [(gbp[i][0], math.log(float(gbp[i][1] / gbp[i - 1][1]))) for i in range(1, len(gbp))]
zero = [m for (m, x) in logs if x == 0.0]
print("changes", len(logs), "exact zero months", zero, "nonzero", len(logs) - len(zero))
# exact zero test on exact Fractions
zero_exact = [gbp[i][0] for i in range(1, len(gbp)) if gbp[i][1] == gbp[i - 1][1]]
print("exact-rate zero months", zero_exact)


def sd(vals):
    n = len(vals)
    m = math.fsum(vals) / n
    return math.sqrt(math.fsum((v - m) ** 2 for v in vals) / (n - 1))


w1 = [x for _, x in logs]
w2 = [x for m, x in logs if m >= "2000-01"]
s1, s2 = sd(w1), sd(w2)
print("n1", len(w1), "sd1", s1, r2(s1, 6), "n2", len(w2), "sd2", s2, r2(s2, 6))
print("diff unrounded", s2 - s1, r2(s2 - s1, 6), "ratio", s2 / s1, r2(s2 / s1, 4))
print("rounded-sd difference (for contrast):", round(0.024700 - 0.027935, 6))
mx1 = max(logs[:], key=lambda t: abs(t[1]))
print("largest window one", mx1, "window two", max([t for t in logs if t[0] >= "2000-01"], key=lambda t: abs(t[1])))
print("log 1.1 =", math.log(1.1), "diff from 0.1:", 0.1 - math.log(1.1))
print("E2 simple change from log -0.0965747:", math.exp(-0.0965747) - 1)
L = math.log(1.1)
print("R2: L (window one largest)=0.135846; h = tanh(L/2) =", math.tanh(0.135846 / 2), "; check ln((1+h)/(1-h)) for h=0.0678:", math.log(1.0678 / 0.9322), "; at h=tanh exact:", math.log((1 + math.tanh(0.135846 / 2)) / (1 - math.tanh(0.135846 / 2))))
print("M2 sd three changes:", sd([0.01, 0.03, -0.02]), "mean", (0.01 + 0.03 - 0.02) / 3)
print("M3 months 2000-01..2026-09 count:", (2026 - 2000) * 12 + (9 - 1) + 1)
print("window two first change rate 1999-12 exists:", any(r_["month"] == "1999-12" for r_ in rows))
