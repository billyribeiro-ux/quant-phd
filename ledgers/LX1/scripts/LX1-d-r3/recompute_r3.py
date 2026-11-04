"""Independent recomputation of every number on cards.json (LX1-d round 3).

Does not import the lab twins. Parses the printed twin outputs only where a card cites a printed
value (to test the printed value against an independent recomputation), and recomputes the
rest from the formulas and from the embedded fx_monthly.csv.

Run: .venv/bin/python -I ledgers/LX1/scripts/LX1-d-r3/recompute_r3.py <repo root>
"""

import csv
import math
import statistics
import sys
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = ROOT / "ledgers/LX1/scripts/LX1-d-r3/out"


def half_up(x: Fraction) -> int:
    return int(Decimal(x.numerator) / Decimal(x.denominator)).__class__(
        (Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal(1), rounding=ROUND_HALF_UP)
    )


def rnd(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


print("== L01 closed form (Theorem 1.3) and the card numbers")
d1, r, g = Fraction(400), Fraction(9, 100), Fraction(3, 100)
F0 = d1 / (r - g)
print("F0 =", F0, "=", float(F0), "rounded", rnd(F0))
print("40000/109 =", float(Fraction(40000, 109)), "rounded", rnd(Fraction(40000, 109)), " 400/1.09 =", Fraction(400) / Fraction(109, 100))
q = (1 + g) / (1 + r)
print("q =", q, float(q))
F2 = d1 * (1 + g) ** 2 / (r - g)
print("F2 =", float(F2), "rounded", rnd(F2))
print("sum S_N(0) identity for N=10,60,200:", [(N, sum(d1 * (1 + g) ** (s - 1) / (1 + r) ** s for s in range(1, N + 1)) == F0 * (1 - q**N)) for N in (10, 60, 200)])
print("d1=400,r=9%,g=1%: F0 =", d1 / (r - Fraction(1, 100)), " P0=6000 gap under 1% =", 6000 - d1 / (r - Fraction(1, 100)), " under 3% =", 6000 - F0)
print("P0=6000 gap under 3% exact =", Fraction(6000) - F0, float(Fraction(6000) - F0))
print("Prop 1.4 witness: any term d1 q^(k-1)/(1+r) >= d1/(1+r) when g>=r; d1/(1+r) =", d1 / (1 + r))
print("Mechanics: F0 at d1=250,r=10%,g=4% =", Fraction(250) / (Fraction(10, 100) - Fraction(4, 100)), "rounded", rnd(Fraction(250) / (Fraction(10, 100) - Fraction(4, 100))))
print("Threshold g* for P0=6000: ", Fraction(9, 100) - Fraction(400, 6000), float(Fraction(9, 100) - Fraction(400, 6000)))

print("== L01 Part B/C: recompute the benchmark-based gap counts from the printed prices (twin printed lines)")
gaps_printed = [-200, 68, 141, 146, 301, 0, -398, 2050, 676, 2175, 2151, -92, 285]
print("positive gaps under 3% (printed prices):", sum(1 for x in gaps_printed if x > 0), "of", len(gaps_printed))
alt_fund = [round(float(Fraction(400) * Fraction(101, 100) ** t / (Fraction(9, 100) - Fraction(1, 100)))) for t in range(13)]
print("alt fundamentals recomputed:", alt_fund[:3], "...", alt_fund[-1])
F3 = [Fraction(400) * (Fraction(103, 100)) ** t / (r - g) for t in range(13)]
fund3 = [rnd(x) for x in F3]
print("3% fundamentals:", fund3)
print("price_t printed (from twin):", [6467, 6935, 7214, 7431, 7804, 7728, 7562, 10249, 9121, 10873, 11110, 9136, 9790])
price = [6467, 6935, 7214, 7431, 7804, 7728, 7562, 10249, 9121, 10873, 11110, 9136, 9790]
print("gaps recomputed from printed prices and fundamentals:", [p - f for p, f in zip(price, fund3)])
print("alt gaps (1%):", [p - a for p, a in zip(price, alt_fund)], "positive:", sum(1 for p, a in zip(price, alt_fund) if p - a > 0))

print("== L02 real value (Prop 2.1), recomputed from the printed index path (Part A)")
P = [Fraction(100), Fraction(99), Fraction(99.99 if False else 0)]  # placeholder replaced below
idx_printed = ["100.0000", "99.0000", "99.9900", "100.9899", "104.0196", "99.8588", "98.8602", "100.8374",
               "96.8039", "93.8998", "96.7168", "98.6511", "94.7051"]
# exact index from the printed change path (-1,+1,+1,+3,-4,-1,+2,-4,-3,+3,+2,-4), the twin's own seeded draw
chg = [-1, 1, 1, 3, -4, -1, 2, -4, -3, 3, 2, -4]
Pex = [Fraction(100)]
for c in chg:
    Pex.append(Pex[-1] * (1 + Fraction(c, 100)))
print("index printed vs recomputed (4dp):", [str(round(float(p), 4)) for p in Pex] == idx_printed)
Vt = [Fraction(1000000) * Fraction(100) / p for p in Pex]
Vcents = [rnd(v) for v in Vt]
print("V_t cents:", Vcents)
print("consecutive V differ in every period:", all(Vcents[t] != Vcents[t - 1] for t in range(1, 13)))
falls = [t for t in range(1, 13) if Pex[t] < Pex[t - 1]]
rises = [t for t in range(1, 13) if Vt[t] > Vt[t - 1]]
print("falls:", falls, len(falls), " rises:", rises, len(rises), " equal sets:", falls == rises)
print("identity exact all t:", all(Vt[t] / Vt[t - 1] == Pex[t - 1] / Pex[t] for t in range(1, 13)))
print("V12/V0 =", float(Vt[12] / Vt[0]), "to 6dp", round(float(Vt[12] / Vt[0]), 6), " P0/P12 =", float(Pex[0] / Pex[12]))
print("E2: V1 from D=1e6, P1=99:", float(Fraction(1000000) * 100 / 99))
print("M1: V1 =", Fraction(2000) * 100 / 80, " M3: V1 =", float(Fraction(200000, 95)))
print("R2 check: D_t P0/P_t", Fraction(1000000) * Pex[3] / 100 * 100 / Pex[3])
print("Remark: ratio of index 100/94.7051 =", 100 / 94.7051)

print("== L03 depth (Prop 3.2(b)) exact, D=1e6, N0=4e6, delta=1/50, phi=beta=1")
D = Fraction(1000000)
N0 = Fraction(4000000)
C = N0 + D
delta = Fraction(1, 50)


def ell(x: Fraction) -> Fraction:
    return x / (C - x)


def depth_formula(m: int) -> Fraction:
    Vm = D * (1 - delta) ** (-m)
    return ell(Vm) - ell(D)


def depth_path(m: int, H: int = 12) -> list[Fraction]:
    out = []
    for t in range(H + 1):
        Pt = (1 - delta) ** min(t, m)
        Vt_ = D / Pt
        Nt = N0 - (Vt_ - D)
        Lt = Vt_ / Nt
        out.append(Lt - D / N0)
    return out


for m in (4, 12):
    path = depth_path(m)
    top = max(path)
    print(f"m={m}: depth exact={float(depth_formula(m)):.6f} (formula) vs path max {float(top):.6f};",
          "first t at max:", path.index(top), " depth % (round half up to 2dp):",
          float(Fraction(rnd(Fraction(100) * top * 100), 100)))
ratio = depth_formula(12) / depth_formula(4)
print("ratio X/Y exact", float(ratio), " to 4dp:", float(Fraction(rnd(ratio * 10000), 10000)))
print("depth X unrounded % =", float(depth_formula(12) * 100), " depth Y unrounded % =", float(depth_formula(4) * 100))
print("V_12 exact =", float(D * (1 - delta) ** (-12)), " rounded", rnd(D * (1 - delta) ** (-12)))
print("V_4 exact =", float(D * (1 - delta) ** (-4)), " P4 =", (1 - delta) ** 4)
for bp in (Fraction(1, 2), Fraction(1), Fraction(3)):
    # depth scales linearly with beta*phi, so the ratio is independent of the product
    print("ratio at product", bp, "=", float(depth_formula(12) * bp / (depth_formula(4) * bp)))

print("== L04 dispersion (fx_monthly.csv, GBP column), recomputed independently with statistics.stdev")
rows = []
with (ROOT / "course/assets/data/market/fx_monthly.csv").open(encoding="utf-8", newline="") as fh:
    for rec in csv.DictReader(fh):
        rows.append((rec["month"], rec["GBP"]))
print("rows:", len(rows), rows[0][0], rows[-1][0], "blank GBP cells:", sum(1 for _, v in rows if v.strip() == ""))
zero_months = []
changes = []
for (m0, v0), (m1, v1) in zip(rows, rows[1:]):
    a, b = Fraction(v0), Fraction(v1)
    if a == b:
        zero_months.append(m1)
    changes.append((m1, math.log(float(b / a))))
print("changes:", len(changes), changes[0][0], changes[-1][0], " exact zero changes:", zero_months)
print("nonzero:", sum(1 for _, c in changes if c != 0.0))
w1 = [c for _, c in changes]
w2 = [c for m, c in changes if m >= "2000-01"]
s1 = statistics.stdev(w1)
s2 = statistics.stdev(w2)
print("n1 =", len(w1), "sd1 =", s1, "to 6dp", f"{s1:.6f}")
print("n2 =", len(w2), "sd2 =", s2, "to 6dp", f"{s2:.6f}")
print("ratio 2/1 =", s2 / s1, "to 4dp", f"{s2 / s1:.4f}")
print("diff 2-1 =", s2 - s1, "to 6dp", f"{s2 - s1:.6f}")
big1 = max(changes, key=lambda t: abs(t[1]))
print("largest abs overall window one:", big1)
b2 = max([t for t in changes if t[0] >= "2000-01"], key=lambda t: abs(t[1]))
print("largest abs window two:", b2, " simple change exp(c)-1 =", math.exp(b2[1]) - 1)
print("ln 1.1 =", math.log(1.1), " 0.1 - ln1.1 =", 0.1 - math.log(1.1))
print("M1 ratio 1.375/1.25 =", Fraction(1375, 1000) / Fraction(125, 100), " ln =", math.log(1.1))
print("window two first change uses 1999-12 rate:", [r_ for r_ in rows if r_[0] in ('1999-12', '2000-01')])
print("months 1971-01..2026-09 count:", len(rows), " 2000-01..2026-09 changes:", len(w2))
