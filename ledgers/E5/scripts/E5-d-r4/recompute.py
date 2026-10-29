"""Independent recomputation of every E5 project number (verifier round 4, slice d).

Written from the page prose and the lab docstrings, not copied from the twins. Uses closed-form OLS
(Sxy / Sxx), exact Fraction means, and the csv module for the snapshot.
"""

import csv
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(sys.argv[1])
SNAP = ROOT / "course/assets/data/market/ust_daily.csv"

QUARTERS = 24
WINDOW = 20
TARGET = 2.0
NATURAL_REAL = 2.0
NATURAL_U = 4.0
PHI_PI = 0.5
PHI_Y = 0.5


def label(k: int) -> str:
    m = 9 + 3 * k
    return f"{2020 + m // 12} Q{(m % 12) // 3 + 1}"


def path(seed: int = 2026):
    r = random.Random(seed)
    gdp = [20000.0]
    for _ in range(23):
        gdp.append(gdp[-1] * (1 + 0.004 + 0.012 * (r.random() - 0.5)))
    price = [100.0]
    for _ in range(23):
        price.append(price[-1] * (1 + 0.005 + 0.004 * (r.random() - 0.5)))
    u = [4.2]
    for _ in range(23):
        u.append(min(7.0, max(3.5, u[-1] + 0.4 * (r.random() - 0.5))))
    pol = [1.0]
    for _ in range(23):
        pol.append(max(0.0, pol[-1] + 0.5 * (r.random() - 0.5)))
    return gdp, price, u, pol


def yields(pol, seed=2027):
    r = random.Random(seed)
    tb = [max(0.0, p + 0.1 * (r.random() - 0.5)) for p in pol]
    cm = [p + 0.8 + 0.8 * (r.random() - 0.5) for p in pol]
    return tb, cm


def ols_trend(gdp, t):
    ys = [math.log(gdp[t - WINDOW + 1 + k]) for k in range(WINDOW)]
    xs = list(range(WINDOW))
    mx = (WINDOW - 1) / 2
    my = sum(ys) / WINDOW
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sxy / sxx
    return my + b * (WINDOW - 1 - mx), b  # fitted value at window's last quarter, slope


def gap_log(gdp, t):
    fit, _ = ols_trend(gdp, t)
    return 100 * (math.log(gdp[t]) - fit)


def gap_pct(gdp, t):
    fit, _ = ols_trend(gdp, t)
    tr = math.exp(fit)
    return 100 * (gdp[t] - tr) / tr


def spreads():
    tot: dict[str, Fraction] = {}
    cnt: dict[str, int] = {}
    blanks = 0
    rows = 0
    first = last = None
    with SNAP.open(encoding="utf-8", newline="") as h:
        rd = csv.reader(h)
        hdr = next(rd)
        assert hdr == ["date", "tbill_3m", "cmt_10y"], hdr
        for rec in rd:
            rows += 1
            d, tb, cm = rec
            first = first or d
            last = d
            if tb == "" or cm == "":
                blanks += 1
                continue
            q = f"{d[:4]} Q{(int(d[5:7]) - 1) // 3 + 1}"
            tot[q] = tot.get(q, Fraction(0)) + Fraction(cm) - Fraction(tb)
            cnt[q] = cnt.get(q, 0) + 1
    return {q: (tot[q] / cnt[q], cnt[q]) for q in tot}, rows, blanks, first, last


gdp, price, u, pol = path()
L = QUARTERS - 1
print("window", label(L - WINDOW + 1), label(L))
sp, rows, blanks, first, last = spreads()
print("snapshot rows", rows, "blank", blanks, "first", first, "last", last)
for t in range(L - 3, L + 1):
    q = label(t)
    g = 100 * ((gdp[t] / gdp[t - 1]) ** 4 - 1)
    pi = 100 * (price[t] / price[t - 4] - 1)
    gl = gap_log(gdp, t)
    gp = gap_pct(gdp, t)
    taylor = NATURAL_REAL + pi + PHI_PI * (pi - TARGET) + PHI_Y * gl
    s, n = sp[q]
    print(
        f"{q} g={g:.6f} pi={pi:.6f} gapLog={gl:.6f} gapPct={gp:.6f} u={u[t]:.6f} pol={pol[t]:.6f} "
        f"taylor={taylor:.6f} polgap={pol[t] - taylor:.6f} spread={float(s):.6f} days={n}"
    )
    print(
        f"  printed g={g:.2f} pi={pi:.2f} gap={gl:.2f} u={u[t]:.2f} pol={pol[t]:.2f} taylor={taylor:.2f} "
        f"polgap={pol[t] - taylor:.2f} spread={float(s):.2f}"
    )

# Lab 2 (completion): latest of 24 pairs
tb, cm = yields(pol)
print("LAB2 pairs", len(tb), "latest tb", f"{tb[-1]:.6f}", "cm", f"{cm[-1]:.6f}", "spread", f"{cm[-1] - tb[-1]:.6f}",
      "printed", f"{cm[-1] - tb[-1]:.2f}")
print("LAB2 gap printed", f"{gap_log(gdp, L):.2f}")

# Exemplar and claim checks
pi_L = 100 * (price[L] / price[L - 4] - 1)
gl_L = gap_log(gdp, L)
tay = NATURAL_REAL + pi_L + PHI_PI * (pi_L - TARGET) + PHI_Y * gl_L
print("TAYLOR unrounded", f"{tay:.9f}", "policy gap", f"{pol[L] - tay:.9f}", "pol", f"{pol[L]:.9f}")
lo = 1 + 1.5 * 1.895 + 0.5 * -0.185
hi = 1 + 1.5 * 1.905 + 0.5 * -0.175
print("TAYLOR bounds from printed-rounding box", f"{lo:.6f}", f"{hi:.6f}")
print("TAYLOR from printed 1.90 and -0.18", f"{1 + 1.5 * 1.90 + 0.5 * -0.18:.6f}")
dphi = 0.5 * gl_L
print("PHI_Y 0.5->1.0 change", f"{dphi:.9f}", "new policy gap", f"{pol[L] - (tay + dphi):.9f}")
print("half gap", f"{gl_L / 2:.9f}")
print("PERCENT vs LOG gap sign same?", (gap_pct(gdp, L) < 0) == (gl_L < 0), f"{gap_pct(gdp, L):.9f}")
print("EXEMPLAR B 2+0.5*gap(Q3)", f"{2 + 0.5 * gl_L:.6f}")
print("EXEMPLAR B 2026 Q2 gap", f"{gap_log(gdp, L - 1):.6f}")

# Lab 1 check on 2 decimals
g_L = 100 * ((gdp[L] / gdp[L - 1]) ** 4 - 1)
print("LAB1 growth", f"{g_L:.9f}", "infl", f"{pi_L:.9f}", "gap", f"{gl_L:.9f}")

# Ask: does D = h(1-c)+bd... not here; only numbers.

# Log-gap vs percent-of-trend gap at all window dates: same sign
bad = [label(t) for t in range(L - WINDOW + 1, L + 1) if (gap_log(gdp, t) < 0) != (gap_pct(gdp, t) < 0)]
print("SIGN MISMATCH dates", bad)
