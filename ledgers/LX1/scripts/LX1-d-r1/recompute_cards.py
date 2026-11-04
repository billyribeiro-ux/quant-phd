"""Independent recomputation of the numbers quoted in LX1 cards (slice d, round 1).

Written without reading the lab twins' code paths; uses Fraction, math and the
embedded snapshot (course/assets/data/market/fx_monthly.csv) and MANIFEST.json.
Run: .venv/bin/python -I ledgers/LX1/scripts/LX1-d-r1/recompute_cards.py
"""
import csv
import json
import math
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE1-LX1-d"


def half_up(x: Fraction) -> int:
    return int(math.floor(x + Fraction(1, 2)))


def show(x: float, places: int) -> str:
    return str(Decimal(repr(x)).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))


# ---- L01 closed form and gaps
d1 = Fraction(400)
r = Fraction(9, 100)
g = Fraction(3, 100)
F0 = d1 / (r - g)
print("c011/c012 F0 (g=3%) =", float(F0), "rounded", half_up(F0))
print("c012 PV of d1 only =", float(d1 / (1 + r)), "=", d1 / (1 + r), "rounded", half_up(d1 / (1 + r)))
print("c011 benchmark g=1% =", float(d1 / (r - Fraction(1, 100))), "; g=3% =", float(d1 / (r - g)))
print("c011 price 6000 gap at 1%:", 6000 - float(d1 / (r - Fraction(1, 100))), "; at 3%:", 6000 - float(F0))
print("c037/c038 L03 check later")
print("L01 L01 M-check Mechanics1 F0(10%,4%,250)=", Fraction(250) / (Fraction(10, 100) - Fraction(4, 100)))

# ---- L02 numbers: none beyond exact algebra; c054/c058 from data below

# ---- L03 model: depths for X (m=12) and Y (m=4), phi=beta=1, delta=1/50, D=1e6, N0=4e6, H=12
D = Fraction(1_000_000)
N0 = Fraction(4_000_000)
delta = Fraction(1, 50)
H = 12


def depth_path(m: int, phi: Fraction = Fraction(1), beta: Fraction = Fraction(1)):
    out = []
    for t in range(H + 1):
        P = (1 - delta) ** min(t, m)
        V = D / P
        Lt = V / (N0 + D - V)
        L0 = D / N0
        out.append(beta * phi * (Lt - L0))
    return out


def depth(m: int, phi=Fraction(1), beta=Fraction(1)) -> Fraction:
    return max(depth_path(m, phi, beta))


dx, dy = depth(12), depth(4)
print("c037 X depth % =", float(100 * dx), "rounded 2dp", show(float(100 * dx), 2), "first t =", depth_path(12).index(dx))
print("c038 Y depth % =", float(100 * dy), "rounded 2dp", show(float(100 * dy), 2), "first t =", depth_path(4).index(dy))
print("L03 E2 difference exact % =", float(100 * (dx - dy)), "9.20-2.69 =", 9.20 - 2.69)
print("c039 ratio X/Y for products 1/2, 1, 3 (phi varies, beta=1):")
for phi in (Fraction(1, 2), Fraction(1), Fraction(3)):
    print("   phi =", phi, "ratio =", float(depth(12, phi) / depth(4, phi)), "->", show(float(depth(12, phi) / depth(4, phi)), 4))
print("L03 M1 P4 =", (Fraction(49, 50)) ** 4, float((Fraction(49, 50)) ** 4))
V4 = D / (Fraction(49, 50)) ** 4
print("L03 M1 V4 =", float(V4), "half-up cents", half_up(V4), "; V12 cents", float(D / (Fraction(49, 50)) ** 12), half_up(D / (Fraction(49, 50)) ** 12))
print("c046 depth at beta=1 =", float(dx))

# ---- L02 numbers
print("c054/c024 L02: Problem E2 V1 =", 1000000 * 100 / 99)

# ---- L04 data: GBP column from the embedded snapshot, independent code path
rows = []
with open(f"{ROOT}/course/assets/data/market/fx_monthly.csv", encoding="utf-8", newline="") as fh:
    rd = csv.DictReader(fh)
    print("fx_monthly header:", rd.fieldnames)
    for rec in rd:
        rows.append((rec["month"], rec["GBP"]))
print("rows =", len(rows), "first", rows[0], "last", rows[-1])
blank = [m for m, v in rows if not v.strip()]
print("blank GBP cells:", blank)
months = [m for m, _ in rows]
vals = [Fraction(v) for _, v in rows]
logs = []
for i in range(1, len(rows)):
    logs.append((months[i], math.log(float(vals[i] / vals[i - 1]))))
print("changes total =", len(logs), "first", logs[0][0], "last", logs[-1][0])
zeros = [m for m, c in logs if c == 0.0]
print("exact-zero changes (float ==0):", zeros, len(zeros))
exact_zero = [months[i] for i in range(1, len(rows)) if vals[i] == vals[i - 1]]
print("exact-zero changes (Fraction equality):", exact_zero)


def sd(xs):
    n = len(xs)
    m = math.fsum(xs) / n
    return math.sqrt(math.fsum((x - m) ** 2 for x in xs) / (n - 1))


w1 = [c for _, c in logs]
w2 = [c for m, c in logs if m >= "2000-01"]
print("w1 n =", len(w1), "sd =", sd(w1), "->", show(sd(w1), 6))
print("w2 n =", len(w2), "sd =", sd(w2), "->", show(sd(w2), 6))
print("w2 - w1 =", sd(w2) - sd(w1), "->", show(sd(w2) - sd(w1), 6))
print("ratio w2/w1 =", sd(w2) / sd(w1), "->", show(sd(w2) / sd(w1), 4))
big1 = max(logs, key=lambda t: abs(t[1]))
print("largest |change| overall:", big1)
big2 = max([t for t in logs if t[0] >= "2000-01"], key=lambda t: abs(t[1]))
print("largest |change| window two:", big2)
print("change 1985-03 and 2008-10:", [t for t in logs if t[0] in ("1985-03", "2008-10")])
print("ln 1.1 =", math.log(1.1), "1.1-ln1.1 =", 0.1 - math.log(1.1))
print("M1 Problem: ln(1.375/1.25)=", math.log(1.375 / 1.25))
print("E2 simple change from log -0.0965747:", math.exp(-0.0965747) - 1)

# ---- MANIFEST checks for fx_daily, ust_daily, fx_monthly
man = json.load(open(f"{ROOT}/course/assets/data/market/MANIFEST.json", encoding="utf-8"))
entries = man.get("snapshots", man) if isinstance(man, dict) else man
print("MANIFEST top-level keys:", list(man.keys()) if isinstance(man, dict) else type(man))
def walk(o, out):
    if isinstance(o, dict):
        if any(k in o for k in ("file", "name", "snapshot")) and any(k in o for k in ("retrieved", "start", "first_date", "coverage")):
            out.append(o)
        for v in o.values():
            walk(v, out)
    elif isinstance(o, list):
        for v in o:
            walk(v, out)
found = []
walk(man, found)
for e in found:
    print("ENTRY", json.dumps(e, ensure_ascii=False)[:600])
