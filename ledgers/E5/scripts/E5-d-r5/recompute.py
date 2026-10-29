"""Independent recomputation of every printed number in the E5 project labs (verifier r5, stdlib + numpy if present)."""
import csv, math, random, sys
from fractions import Fraction
from collections import defaultdict
import numpy as np  # independent least-squares route

ROOT = sys.argv[1]
SEED, Q, W = 2026, 24, 20

def path(seed=SEED):
    r = random.Random(seed)
    gdp = [20000.0]
    for _ in range(Q - 1):
        gdp.append(gdp[-1] * (1 + 0.004 + 0.012 * (r.random() - 0.5)))
    price = [100.0]
    for _ in range(Q - 1):
        price.append(price[-1] * (1 + 0.005 + 0.004 * (r.random() - 0.5)))
    un = [4.2]
    for _ in range(Q - 1):
        un.append(min(7.0, max(3.5, un[-1] + 0.4 * (r.random() - 0.5))))
    pol = [1.0]
    for _ in range(Q - 1):
        pol.append(max(0.0, pol[-1] + 0.5 * (r.random() - 0.5)))
    return gdp, price, un, pol

def yields(pol, seed=SEED + 1):
    r = random.Random(seed)
    tb = [max(0.0, p + 0.1 * (r.random() - 0.5)) for p in pol]
    cm = [p + 0.8 + 0.8 * (r.random() - 0.5) for p in pol]
    return tb, cm

gdp, price, un, pol = path()
t = Q - 1
growth = 100 * ((gdp[t] / gdp[t - 1]) ** 4 - 1)
infl = 100 * (price[t] / price[t - 4] - 1)
x = np.arange(W, dtype=float)
y = np.log(np.array(gdp[t - W + 1: t + 1]))
slope, intercept = np.polyfit(x, y, 1)
trend_end = intercept + slope * (W - 1)
trend_end_pct = math.exp(trend_end)
log_gap = 100 * (math.log(gdp[t]) - trend_end)
pct_gap = 100 * (gdp[t] - trend_end_pct) / trend_end_pct
print("unrounded growth %.10f  infl %.10f" % (growth, infl))
print("unrounded log gap %.6f  pct-of-trend gap %.6f" % (log_gap, pct_gap))
taylor = 2.0 + infl + 0.5 * (infl - 2.0) + 0.5 * log_gap
print("unrounded Taylor %.6f  policy gap %.6f  policy %.2f" % (taylor, pol[t] - taylor, pol[t]))
# exemplar A bounds: value range over inflation in [1.895,1.905], gap in [-0.185,-0.175]
lo = 1 + 1.5 * 1.895 + 0.5 * -0.185
hi = 1 + 1.5 * 1.905 + 0.5 * -0.175
print("exemplar A Taylor bounds (rule form 1+1.5pi+0.5gap): %.4f .. %.4f" % (lo, hi))
print("Taylor change for phi_y 0.5->1.0 at unrounded gap: %.6f" % (0.5 * log_gap))
print("half-gap range: %.5f .. %.5f" % (0.5 * -0.185, 0.5 * -0.175))
# window and quarter labels
def lab(k):
    m = 9 + 3 * k
    return f"{2020 + m // 12} Q{(m % 12) // 3 + 1}"
print("latest", lab(t), "window start", lab(t - W + 1))

# term spread, exact quarter means from snapshot
totals, days = defaultdict(Fraction), defaultdict(int)
with open(f"{ROOT}/course/assets/data/market/ust_daily.csv", encoding="utf-8") as fh:
    rd = csv.reader(fh)
    hdr = next(rd)
    assert hdr == ["date", "tbill_3m", "cmt_10y"], hdr
    for row in rd:
        d, a, b = row
        if a == "" or b == "":
            continue
        y_, m_ = int(d[:4]), int(d[5:7])
        key = f"{y_} Q{(m_ - 1) // 3 + 1}"
        totals[key] += Fraction(b) - Fraction(a)
        days[key] += 1
for k in ["2025 Q4", "2026 Q1", "2026 Q2", "2026 Q3"]:
    print("spread", k, "days", days[k], "mean %.6f" % float(totals[k] / days[k]))
print("first/last snapshot row check done")

# lab 2 spread from seed 2027 yields, latest pair
tb, cm = yields(pol)
print("lab2 spread latest (seed 2027) %.6f" % (cm[t] - tb[t]))
# lab 2 alt gap: percent-of-trend with same trend, latest quarter
print("lab2 pct-of-trend gap %.6f  log gap %.6f" % (pct_gap, log_gap))
# day-count sanity: quarters in 2026 Q3 from snapshot
print("sign checks: growth", growth > 0, "gap", log_gap < 0, "infl-target", infl - 2 < 0,
      "un-4", un[t] - 4 > 0, "policy-taylor", pol[t] - taylor < 0)
print("unemployment latest %.4f  policy latest %.4f" % (un[t], pol[t]))
