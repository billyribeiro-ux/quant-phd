"""Independent recomputation (H1, E5-d closing delta) of the numbers the changed prose states.
Run from the checkout root: python -I h1_numbers.py"""
import csv, math, random
from fractions import Fraction

def path(seed=2026, q=24):
    rng = random.Random(seed)
    gdp = [20000.0]
    for _ in range(q - 1):
        gdp.append(gdp[-1] * (1 + 0.004 + 0.012 * (rng.random() - 0.5)))
    price = [100.0]
    for _ in range(q - 1):
        price.append(price[-1] * (1 + 0.005 + 0.004 * (rng.random() - 0.5)))
    un = [4.2]
    for _ in range(q - 1):
        un.append(min(7.0, max(3.5, un[-1] + 0.4 * (rng.random() - 0.5))))
    pol = [1.0]
    for _ in range(q - 1):
        pol.append(max(0.0, pol[-1] + 0.5 * (rng.random() - 0.5)))
    return gdp, price, un, pol

def trend(gdp, t, W=20):
    first = t - W + 1
    xs = [float(k) for k in range(W)]
    ys = [math.log(gdp[first + k]) for k in range(W)]
    xb = sum(xs) / W; yb = sum(ys) / W
    s = sum((x - xb) * (y - yb) for x, y in zip(xs, ys)) / sum((x - xb) ** 2 for x in xs)
    return yb - s * xb, s

gdp, price, un, pol = path()
T = 23
a, s = trend(gdp, T)
trend_end = a + s * 19
log_gap = 100 * (math.log(gdp[T]) - trend_end)
pct_gap = 100 * (gdp[T] - math.exp(trend_end)) / math.exp(trend_end)
print("log gap (conventions, 2026 Q3):", repr(log_gap), f"{log_gap:.2f}")
print("percent-of-trend gap:", repr(pct_gap), f"{pct_gap:.2f}")
print("same sign:", (log_gap > 0) == (pct_gap > 0))

# Rung 1 / Lab 3 table values
def gap_at(t):
    a, s = trend(gdp, t); return 100 * (math.log(gdp[t]) - (a + s * 19))
growth = 100 * ((gdp[T] / gdp[T - 1]) ** 4 - 1)
infl = 100 * (price[T] / price[T - 4] - 1)
g = gap_at(T)
taylor = 2.0 + infl + 0.5 * (infl - 2.0) + 0.5 * g
print("growth %.6f inflation %.6f gap %.6f taylor %.6f policy gap %.6f" % (growth, infl, g, taylor, pol[T] - taylor))
print("unemployment %.4f policy %.4f" % (un[T], pol[T]))
# Taylor range from unrounded bounds in the memo
for pi_ in (1.895, 1.905):
    for gg in (-0.185, -0.175):
        print("taylor bound", pi_, gg, round(2 + pi_ + 0.5 * (pi_ - 2) + 0.5 * gg, 4))
print("phi_y 1.0 change of taylor = 0.5*gap =", 0.5 * g, " policy gap after:", pol[T] - (taylor + 0.5 * g))

# Lab 3 term spreads from the snapshot
rows = list(csv.reader(open("course/assets/data/market/ust_daily.csv", encoding="utf-8")))
hdr = rows[0]
print("header", hdr, "rows", len(rows) - 1, "first", rows[1][0], "last", rows[-1][0])
tot = {}; cnt = {}
for r in rows[1:]:
    d, tb, cm = r[0], r[1], r[2]
    if tb == "" or cm == "":
        continue
    lab = f"{int(d[:4])} Q{(int(d[5:7]) - 1) // 3 + 1}"
    tot[lab] = tot.get(lab, Fraction(0)) + (Fraction(cm) - Fraction(tb))
    cnt[lab] = cnt.get(lab, 0) + 1
for lab in ["2025 Q4", "2026 Q1", "2026 Q2", "2026 Q3"]:
    print("spread", lab, cnt.get(lab), float(tot[lab] / cnt[lab]))
print("spread 2026 Q3 two-decimal:", f"{float(tot['2026 Q3'] / cnt['2026 Q3']):.2f}")

# Lab 2 E3 unrounded average of dlnK (L02), seeded economy random.Random(2026)
rng = random.Random(2026)
A = [1.0]; K = [100.0]; L = [50.0]
for _ in range(40):
    A.append(A[-1] * math.exp(rng.uniform(0.005, 0.02)))
    K.append(K[-1] * math.exp(rng.uniform(0.02, 0.05)))
    L.append(L[-1] * math.exp(rng.uniform(0.0, 0.015)))
dk = [math.log(K[t]) - math.log(K[t - 1]) for t in range(1, 41)]
dl = [math.log(L[t]) - math.log(L[t - 1]) for t in range(1, 41)]
print("avg dlnK %.10f  avg dlnL %.10f" % (sum(dk) / 40, sum(dl) / 40))
print("0.4*avgdlnK unrounded %.8f ; rounded-intermediate 0.4*0.035557 = %.6f" % (0.4 * sum(dk) / 40, 0.4 * 0.035557))
print("0.3*avgdlnK =", 0.3 * sum(dk) / 40, " 0.7*avgdlnL =", 0.7 * sum(dl) / 40)

# Lab 3 table rows 2025 Q4 .. 2026 Q3 (independent recompute)
for t in range(20, 24):
    lab = f"{2020 + (9 + 3 * t) // 12} Q{((9 + 3 * t) % 12) // 3 + 1}"
    gr = 100 * ((gdp[t] / gdp[t - 1]) ** 4 - 1)
    inf = 100 * (price[t] / price[t - 4] - 1)
    a2, s2 = trend(gdp, t)
    gp = 100 * (math.log(gdp[t]) - (a2 + s2 * 19))
    tay = 2.0 + inf + 0.5 * (inf - 2.0) + 0.5 * gp
    print(f"{lab} | {gr:.2f} | {inf:.2f} | {gp:.2f} | {un[t]:.2f} | {pol[t]:.2f} | {tay:.2f} | {pol[t] - tay:.2f} | {tot[lab] / cnt[lab]:.2f}".replace("| ", "| "))

# Card numbers (cards c019, c020, c021, c022, c035, c051, c052)
print("c019 ln1.25 %.6f ; 0.25 - ln1.25 %.6f" % (math.log(1.25), 0.25 - math.log(1.25)))
print("c020 nominal 105/995 %.6f ; deflator 4/23 %.6f ; real growth (1100/995)/(27/23)-1 %.6f" % (105 / 995, 4 / 23, (1100 / 995) / (27 / 23) - 1))
print("c021 private saving %d public %d total %d" % (1010 - 230 - 620, 230 - 210, (1010 - 230 - 620) + (230 - 210)))
print("c022 basket A P^L %s P^P %s gap %s" % ("5/4", "27/23", "7/92"))
print("c035 1.1^0.3 %.6f ; simple %.6f ; 0.3 ln1.1 %.6f" % (1.1 ** 0.3, 1.1 ** 0.3 - 1, 0.3 * math.log(1.1)))
print("c051 10/7 %.10f" % (10 / 7))
print("c052 k* %.10f ; (k*)^0.3 %.10f" % ((10 / 3) ** (10 / 7), ((10 / 3) ** (10 / 7)) ** 0.3))
