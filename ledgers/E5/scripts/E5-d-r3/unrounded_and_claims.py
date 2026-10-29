"""Independent recomputation of project.html numbers (E5 slice d, round 3). Run: python3 -I this.py <repo-root>"""
import math, random, sys
from fractions import Fraction
from pathlib import Path

root = Path(sys.argv[1])
SEED, Q, W = 2026, 24, 20


def path(seed=SEED):
    rng = random.Random(seed)
    gdp = [20000.0]
    for _ in range(Q - 1):
        gdp.append(gdp[-1] * (1 + 0.004 + 0.012 * (rng.random() - 0.5)))
    price = [100.0]
    for _ in range(Q - 1):
        price.append(price[-1] * (1 + 0.005 + 0.004 * (rng.random() - 0.5)))
    un = [4.2]
    for _ in range(Q - 1):
        un.append(min(7.0, max(3.5, un[-1] + 0.4 * (rng.random() - 0.5))))
    pol = [1.0]
    for _ in range(Q - 1):
        pol.append(max(0.0, pol[-1] + 0.5 * (rng.random() - 0.5)))
    return gdp, price, un, pol


def lab(k):
    m = 9 + 3 * k
    return f"{2020 + m // 12} Q{(m % 12) // 3 + 1}"


def trend(gdp, t):
    first = t - W + 1
    xs = list(range(W))
    ys = [math.log(gdp[first + k]) for k in range(W)]
    xb, yb = sum(xs) / W, sum(ys) / W
    b = sum((x - xb) * (y - yb) for x, y in zip(xs, ys)) / sum((x - xb) ** 2 for x in xs)
    return yb - b * xb, b


gdp, price, un, pol = path()
# yields exactly as the twin does (seed 2027, from policy path)
rng = random.Random(SEED + 1)
tbill = [max(0.0, p + 0.1 * (rng.random() - 0.5)) for p in pol]
cmt = [p + 0.8 + 0.8 * (rng.random() - 0.5) for p in pol]

# spreads from snapshot, exact
totals, days, first_d, last_d, n_rows, blank = {}, {}, None, None, 0, 0
with (root / "course/assets/data/market/ust_daily.csv").open() as h:
    hdr = next(h).strip().split(",")
    print("HEADER", hdr)
    for line in h:
        d, tb, c = line.strip().split(",")
        n_rows += 1
        if first_d is None:
            first_d = d
        last_d = d
        if tb == "" or c == "":
            blank += 1
            continue
        lab_ = f"{int(d[:4])} Q{(int(d[5:7]) - 1) // 3 + 1}"
        totals[lab_] = totals.get(lab_, Fraction(0)) + Fraction(c) - Fraction(tb)
        days[lab_] = days.get(lab_, 0) + 1
print("SNAPSHOT rows", n_rows, "first", first_d, "last", last_d, "blank-skipped", blank)
for q in ["2025 Q4", "2026 Q1", "2026 Q2", "2026 Q3"]:
    print("SPREAD", q, "days", days[q], "mean_pp_unrounded", float(totals[q] / days[q]), "printed", f"{float(totals[q]/days[q]):.2f}")

L = Q - 1
for t in range(L - 3, L + 1):
    g = 100 * ((gdp[t] / gdp[t - 1]) ** 4 - 1)
    pi = 100 * (price[t] / price[t - 4] - 1)
    a, b = trend(gdp, t)
    ylog = 100 * (math.log(gdp[t]) - (a + b * (W - 1)))
    trend_level = math.exp(a + b * (W - 1))
    ypct = 100 * (gdp[t] - trend_level) / trend_level
    tay = 2.0 + pi + 0.5 * (pi - 2.0) + 0.5 * ylog
    sp = float(totals[lab(t)] / days[lab(t)])
    print(f"ROW {lab(t)} g={g!r} pi={pi!r} ylog={ylog!r} ypct={ypct!r} taylor={tay!r} policy_gap={pol[t]-tay!r} spread={sp!r} u={un[t]!r} i={pol[t]!r}")
    print(f"   printed: g={g:.2f} pi={pi:.2f} ylog={ylog:.2f} taylor={tay:.2f} gap={pol[t]-tay:.2f} u={un[t]:.2f} i={pol[t]:.2f} spread={sp:.2f}")

# Claims in conventions: log gap and percent gap at 2026 Q3
a, b = trend(gdp, L)
ylog = 100 * (math.log(gdp[L]) - (a + b * (W - 1)))
tl = math.exp(a + b * (W - 1))
ypct = 100 * (gdp[L] - tl) / tl
print("CLAIM log gap", f"{ylog:.5f}", "percent gap", f"{ypct:.5f}")
pi_L = 100 * (price[L] / price[L - 4] - 1)
g_L = 100 * ((gdp[L] / gdp[L - 1]) ** 4 - 1)
print("UNROUNDED 2026Q3 g", g_L, "pi", pi_L)
tay_L = 2.0 + pi_L + 0.5 * (pi_L - 2.0) + 0.5 * ylog
print("TAYLOR 2026Q3 unrounded", tay_L, "policy gap", pol[L] - tay_L, "policy", pol[L])
print("EXEMPLAR A: taylor from printed inputs", 2.0 + 1.90 + 0.5 * (1.90 - 2.0) + 0.5 * (-0.18))
print("EXEMPLAR A: range inputs", 2.0 + 1.895 + 0.5 * (1.895 - 2) + 0.5 * (-0.185), 2.0 + 1.905 + 0.5 * (1.905 - 2) + 0.5 * (-0.175))
print("EXEMPLAR A: 0.5*gap change with phi_y 0.5->1.0 (unrounded gap)", 0.5 * ylog, "policy gap after", pol[L] - (tay_L + 0.5 * ylog))
print("EXEMPLAR A: half-gap range", 0.5 * -0.185, 0.5 * -0.175)
print("EXEMPLAR B: 2 + 0.5*gap", 2 + 0.5 * (-0.18))
print("PARAM policy printed 1.53 rounds from", pol[L])
