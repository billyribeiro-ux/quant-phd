# Independent recomputation of the E5 project default state (verifier scratch; not part of the repo).
import sys, random, math
from fractions import Fraction
import numpy as np
from datetime import date
sys.path.insert(0, "/tmp/verifyC1-E5-d/.venv/lib/python3.14/site-packages")
# --- own generator, written from the page's description (seed 2026, 24 quarters)
rng = random.Random(2026)
gdp = [20000.0]
for _ in range(23):
    gdp.append(gdp[-1] * (1 + 0.004 + 0.012 * (rng.random() - 0.5)))
price = [100.0]
for _ in range(23):
    price.append(price[-1] * (1 + 0.005 + 0.004 * (rng.random() - 0.5)))
un = [4.2]
for _ in range(23):
    un.append(min(7.0, max(3.5, un[-1] + 0.4 * (rng.random() - 0.5))))
pol = [1.0]
for _ in range(23):
    pol.append(max(0.0, pol[-1] + 0.5 * (rng.random() - 0.5)))
t = 23
g = 100 * ((gdp[t] / gdp[t-1]) ** 4 - 1)
pi = 100 * (price[t] / price[t-4] - 1)
# trend via numpy polyfit on window (independent algorithm), evaluated at last point
ys = np.log(np.array(gdp[t-19:t+1]))
slope, icpt = np.polyfit(np.arange(20), ys, 1)
gap = 100 * (math.log(gdp[t]) - (icpt + slope * 19))
taylor = 2 + pi + 0.5 * (pi - 2) + 0.5 * gap
print("growth", repr(g), "infl", repr(pi), "gap", repr(gap), "taylor", repr(taylor), "policy", pol[t], "policy gap", pol[t]-taylor, "un", un[t])
print("unrounded growth %.4f infl %.4f gap %.4f taylor %.4f policygap %.4f" % (g, pi, gap, taylor, pol[t]-taylor))
# --- spreads from snapshot, exact Fractions, own parser
rows = open("/tmp/verifyC1-E5-d/course/assets/data/market/ust_daily.csv", encoding="utf-8").read().splitlines()
print("header:", rows[0]); print("first:", rows[1]); print("last:", rows[-1]); print("nrows:", len(rows)-1)
bad = [r for r in rows[1:] if any(x.strip() == "" for x in r.split(","))]
print("rows with empty field:", len(bad), bad[:3])
q = {}
for r in rows[1:]:
    d, tb, cm = r.split(",")
    y, m = int(d[:4]), int(d[5:7])
    key = (y, (m-1)//3+1)
    q.setdefault(key, []).append(Fraction(cm) - Fraction(tb))
for key in [(2025,4),(2026,1),(2026,2),(2026,3)]:
    v = q[key]
    print(key, "days", len(v), "mean", float(sum(v)/len(v)), "%.4f" % float(sum(v)/len(v)))
print("date range", rows[1].split(",")[0], rows[-1].split(",")[0])
# non-decimal or negative check
print("nonnumeric:", sum(1 for r in rows[1:] for x in r.split(",")[1:] if not x.replace('.','',1).replace('-','',1).isdigit()))
